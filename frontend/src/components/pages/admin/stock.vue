<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BaseButton from '../../UI/BaseButton.vue'
import BaseCard from '../../UI/BaseCard.vue'
import BaseModal from '../../UI/BaseModal.vue'
import BaseInput from '../../UI/BaseInput.vue'

const books = ref<any[]>([])
const authors = ref<any[]>([])
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const showBookModal = ref(false)
const showAuthorModal = ref(false)
const editingBook = ref<any>(null)
const editingAuthor = ref<any>(null)

const bookForm = ref({ title: '', author_id: '', country: '', publication_year: 2000, genre: '', description: '' })
const authorForm = ref({ name: '', country: '', birth_year: 1900, death_year: null as number | null, biography: '' })

async function loadData() {
  try {
    const [booksRes, authorsRes] = await Promise.all([
      fetch(`${apiBase}/books`),
      fetch(`${apiBase}/authors`)
    ])
    books.value = await booksRes.json()
    authors.value = await authorsRes.json()
  } catch (e) {
    console.error('Error:', e)
  }
}

function getAuthorName(authorId: string): string {
  return authors.value.find(a => a.id === authorId)?.name || '—'
}

function openCreateBook() {
  editingBook.value = null
  bookForm.value = { title: '', author_id: authors.value[0]?.id || '', country: '', publication_year: 2000, genre: '', description: '' }
  showBookModal.value = true
}

function openEditBook(book: any) {
  editingBook.value = book
  bookForm.value = { title: book.title, author_id: book.author_id, country: book.country, publication_year: book.publication_year, genre: book.genre, description: book.description || '' }
  showBookModal.value = true
}

function openCreateAuthor() {
  editingAuthor.value = null
  authorForm.value = { name: '', country: '', birth_year: 1900, death_year: null, biography: '' }
  showAuthorModal.value = true
}

function openEditAuthor(author: any) {
  editingAuthor.value = author
  authorForm.value = { name: author.name, country: author.country, birth_year: author.birth_year, death_year: author.death_year, biography: author.biography || '' }
  showAuthorModal.value = true
}

async function saveBook() {
  try {
    const body = JSON.stringify(bookForm.value)
    const bytes = new TextEncoder().encode(body)
    if (editingBook.value) {
      await fetch(`${apiBase}/books/${editingBook.value.id}`, { method: 'PUT', body: bytes, headers: { 'Content-Type': 'application/json' } })
    } else {
      await fetch(`${apiBase}/books`, { method: 'POST', body: bytes, headers: { 'Content-Type': 'application/json' } })
    }
    showBookModal.value = false
    loadData()
  } catch (e) { console.error(e) }
}

async function deleteBook(id: string) {
  try {
    await fetch(`${apiBase}/books/${id}`, { method: 'DELETE' })
    loadData()
  } catch (e) { console.error(e) }
}

async function saveAuthor() {
  try {
    const body = JSON.stringify(authorForm.value)
    const bytes = new TextEncoder().encode(body)
    if (editingAuthor.value) {
      await fetch(`${apiBase}/authors/${editingAuthor.value.id}`, { method: 'PUT', body: bytes, headers: { 'Content-Type': 'application/json' } })
    } else {
      await fetch(`${apiBase}/authors`, { method: 'POST', body: bytes, headers: { 'Content-Type': 'application/json' } })
    }
    showAuthorModal.value = false
    loadData()
  } catch (e) { console.error(e) }
}

async function deleteAuthor(id: string) {
  try {
    await fetch(`${apiBase}/authors/${id}`, { method: 'DELETE' })
    loadData()
  } catch (e) { console.error(e) }
}

onMounted(loadData)
</script>

<template>
  <div>
    <!-- Books section -->
    <div class="flex items-center justify-between mb-5">
      <h1 class="text-2xl">Libros</h1>
      <BaseButton @click="openCreateBook">+ Nuevo libro</BaseButton>
    </div>

    <BaseCard variant="outlined" padding="none">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-rule bg-paper-2/50">
              <th class="text-left px-5 py-3 text-ink-3 font-medium">Título</th>
              <th class="text-left px-5 py-3 text-ink-3 font-medium">Autor</th>
              <th class="text-left px-5 py-3 text-ink-3 font-medium">País</th>
              <th class="text-left px-5 py-3 text-ink-3 font-medium">Año</th>
              <th class="text-left px-5 py-3 text-ink-3 font-medium">Género</th>
              <th class="text-right px-5 py-3 text-ink-3 font-medium">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book.id" class="border-b border-rule/50 hover:bg-paper-2/30 transition-colors">
              <td class="px-5 py-3 text-ink font-medium">{{ book.title }}</td>
              <td class="px-5 py-3 text-ink-2">{{ getAuthorName(book.author_id) }}</td>
              <td class="px-5 py-3 text-ink-2">{{ book.country }}</td>
              <td class="px-5 py-3 font-[var(--font-mono)] text-ink-2">{{ book.publication_year }}</td>
              <td class="px-5 py-3 text-ink-2">{{ book.genre }}</td>
              <td class="px-5 py-3 text-right">
                <div class="flex items-center justify-end gap-2">
                  <BaseButton variant="ghost" size="sm" @click="openEditBook(book)">Editar</BaseButton>
                  <BaseButton variant="danger" size="sm" @click="deleteBook(book.id)">Eliminar</BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <!-- Authors section -->
    <div class="flex items-center justify-between mt-12 mb-5">
      <h1 class="text-2xl">Autores</h1>
      <BaseButton @click="openCreateAuthor">+ Nuevo autor</BaseButton>
    </div>

    <BaseCard variant="outlined" padding="none">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-rule bg-paper-2/50">
              <th class="text-left px-5 py-3 text-ink-3 font-medium">Nombre</th>
              <th class="text-left px-5 py-3 text-ink-3 font-medium">País</th>
              <th class="text-left px-5 py-3 text-ink-3 font-medium">Nacimiento</th>
              <th class="text-left px-5 py-3 text-ink-3 font-medium">Fallecimiento</th>
              <th class="text-right px-5 py-3 text-ink-3 font-medium">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="author in authors" :key="author.id" class="border-b border-rule/50 hover:bg-paper-2/30 transition-colors">
              <td class="px-5 py-3 text-ink font-medium">{{ author.name }}</td>
              <td class="px-5 py-3 text-ink-2">{{ author.country }}</td>
              <td class="px-5 py-3 font-[var(--font-mono)] text-ink-2">{{ author.birth_year }}</td>
              <td class="px-5 py-3 font-[var(--font-mono)] text-ink-2">{{ author.death_year || '—' }}</td>
              <td class="px-5 py-3 text-right">
                <div class="flex items-center justify-end gap-2">
                  <BaseButton variant="ghost" size="sm" @click="openEditAuthor(author)">Editar</BaseButton>
                  <BaseButton variant="danger" size="sm" @click="deleteAuthor(author.id)">Eliminar</BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <!-- Book Modal -->
    <BaseModal :open="showBookModal" :title="editingBook ? 'Editar libro' : 'Nuevo libro'" @close="showBookModal = false">
      <form @submit.prevent="saveBook" class="flex flex-col gap-4">
        <BaseInput v-model="bookForm.title" label="Título" placeholder="Título del libro" required />
        <div class="grid grid-cols-2 gap-3">
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-ink-2">Autor</label>
            <select v-model="bookForm.author_id" class="px-4 py-2.5 bg-paper border border-rule rounded-[var(--radius-md)] text-ink text-sm focus:outline-none focus:border-accent">
              <option v-for="a in authors" :key="a.id" :value="a.id">{{ a.name }}</option>
            </select>
          </div>
          <BaseInput v-model="bookForm.country" label="País" placeholder="País" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <BaseInput v-model.number="bookForm.publication_year" label="Año" type="number" />
          <BaseInput v-model="bookForm.genre" label="Género" placeholder="Género" />
        </div>
        <div class="flex justify-end gap-3 mt-2">
          <BaseButton variant="ghost" type="button" @click="showBookModal = false">Cancelar</BaseButton>
          <BaseButton type="submit">{{ editingBook ? 'Guardar' : 'Crear' }}</BaseButton>
        </div>
      </form>
    </BaseModal>

    <!-- Author Modal -->
    <BaseModal :open="showAuthorModal" :title="editingAuthor ? 'Editar autor' : 'Nuevo autor'" @close="showAuthorModal = false">
      <form @submit.prevent="saveAuthor" class="flex flex-col gap-4">
        <BaseInput v-model="authorForm.name" label="Nombre" placeholder="Nombre del autor" required />
        <BaseInput v-model="authorForm.country" label="País" placeholder="País" />
        <div class="grid grid-cols-2 gap-3">
          <BaseInput v-model.number="authorForm.birth_year" label="Año nacimiento" type="number" />
          <BaseInput v-model.number="authorForm.death_year" label="Año fallecimiento" type="number" />
        </div>
        <div class="flex justify-end gap-3 mt-2">
          <BaseButton variant="ghost" type="button" @click="showAuthorModal = false">Cancelar</BaseButton>
          <BaseButton type="submit">{{ editingAuthor ? 'Guardar' : 'Crear' }}</BaseButton>
        </div>
      </form>
    </BaseModal>
  </div>
</template>
