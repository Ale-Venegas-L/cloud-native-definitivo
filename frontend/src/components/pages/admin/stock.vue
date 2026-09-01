<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import BaseButton from '../../UI/BaseButton.vue'
import BaseCard from '../../UI/BaseCard.vue'
import BaseModal from '../../UI/BaseModal.vue'
import BaseInput from '../../UI/BaseInput.vue'
import ContentState from '../../UI/ContentState.vue'
import EditorialCover from '../../UI/EditorialCover.vue'
import { apiRequest } from '../../../services/api'
import { editionForBook } from '../../../data/editions'
import type { Author, AuthorPayload, Book, BookPayload } from '../../../types/domain'

type DeleteTarget = { kind: 'book' | 'author'; id: string; label: string }
const route = useRoute()
const books = ref<Book[]>([]), authors = ref<Author[]>([])
const activeTab = ref<'books' | 'authors'>('books'), search = ref('')
const loading = ref(true), saving = ref(false), operationError = ref('')
const showBookModal = ref(false), showAuthorModal = ref(false)
const editingBook = ref<Book | null>(null), editingAuthor = ref<Author | null>(null)
const deleteTarget = ref<DeleteTarget | null>(null)
const bookForm = ref<BookPayload>({ title: '', author_id: '', country: '', publication_year: 2000, genre: '', description: '', cover_url: '' })
const authorForm = ref<AuthorPayload>({ name: '', country: '', birth_year: 1900, death_year: null, biography: '', image_url: '' })
const previewEdition = computed(() => editionForBook(bookForm.value.title))
const filteredBooks = computed(() => books.value.filter(book => `${book.title} ${authorName(book.author_id)} ${book.genre}`.toLocaleLowerCase('es').includes(search.value.toLocaleLowerCase('es'))))
const filteredAuthors = computed(() => authors.value.filter(author => `${author.name} ${author.country}`.toLocaleLowerCase('es').includes(search.value.toLocaleLowerCase('es'))))

async function loadData() {
  loading.value = true
  try { [books.value, authors.value] = await Promise.all([apiRequest<Book[]>('/books/'), apiRequest<Author[]>('/authors/')]); operationError.value = '' }
  catch (e) { operationError.value = message(e, 'No fue posible cargar los datos') }
  finally { loading.value = false }
}
function message(error: unknown, fallback: string) { return error instanceof Error ? error.message : fallback }
function authorName(id: string) { return authors.value.find(author => author.id === id)?.name || '—' }
function openCreateBook() { editingBook.value = null; bookForm.value = { title: '', author_id: authors.value[0]?.id || '', country: '', publication_year: new Date().getFullYear(), genre: '', description: '', cover_url: '' }; operationError.value = ''; showBookModal.value = true }
function openEditBook(book: Book) { editingBook.value = book; bookForm.value = { title: book.title, author_id: book.author_id, country: book.country, publication_year: book.publication_year, genre: book.genre, description: book.description || '', cover_url: book.cover_url || '' }; operationError.value = ''; showBookModal.value = true }
function openCreateAuthor() { editingAuthor.value = null; authorForm.value = { name: '', country: '', birth_year: 1900, death_year: null, biography: '', image_url: '' }; operationError.value = ''; showAuthorModal.value = true }
function openEditAuthor(author: Author) { editingAuthor.value = author; authorForm.value = { name: author.name, country: author.country, birth_year: author.birth_year, death_year: author.death_year, biography: author.biography || '', image_url: author.image_url || '' }; operationError.value = ''; showAuthorModal.value = true }
async function saveBook() {
  saving.value = true; operationError.value = ''
  try { await apiRequest<Book>(editingBook.value ? `/books/${editingBook.value.id}` : '/books/', { method: editingBook.value ? 'PUT' : 'POST', body: JSON.stringify(bookForm.value), authenticated: true }); showBookModal.value = false; await loadData() }
  catch (e) { operationError.value = message(e, 'No fue posible guardar el libro') }
  finally { saving.value = false }
}
async function saveAuthor() {
  saving.value = true; operationError.value = ''
  try { await apiRequest<Author>(editingAuthor.value ? `/authors/${editingAuthor.value.id}` : '/authors/', { method: editingAuthor.value ? 'PUT' : 'POST', body: JSON.stringify(authorForm.value), authenticated: true }); showAuthorModal.value = false; await loadData() }
  catch (e) { operationError.value = message(e, 'No fue posible guardar el autor') }
  finally { saving.value = false }
}
async function confirmDelete() {
  if (!deleteTarget.value) return
  saving.value = true; operationError.value = ''
  try { await apiRequest<void>(`/${deleteTarget.value.kind === 'book' ? 'books' : 'authors'}/${deleteTarget.value.id}`, { method: 'DELETE', authenticated: true }); deleteTarget.value = null; await loadData() }
  catch (e) { operationError.value = message(e, 'No fue posible eliminar el registro'); deleteTarget.value = null }
  finally { saving.value = false }
}
onMounted(async () => { await loadData(); if (route.query.create === 'book') openCreateBook(); if (route.query.create === 'author') { activeTab.value = 'authors'; openCreateAuthor() } })
</script>

<template>
  <div>
    <div class="mb-7"><p class="mb-2 text-xs font-semibold uppercase tracking-[.15em] text-accent">Gestión de contenido</p><h1 class="text-3xl sm:text-4xl">Biblioteca</h1><p class="mt-2 text-sm text-ink-3">Administra obras y autores desde un solo lugar.</p></div>
    <div v-if="operationError" class="mb-5 flex items-start justify-between gap-3 rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger" role="alert"><span>{{ operationError }}</span><button type="button" aria-label="Cerrar error" @click="operationError = ''">×</button></div>
    <div class="mb-6 flex flex-col gap-4 border-b border-rule sm:flex-row sm:items-end sm:justify-between">
      <div class="flex gap-5"><button v-for="tab in [{ id: 'books', label: `Libros (${books.length})` }, { id: 'authors', label: `Autores (${authors.length})` }]" :key="tab.id" type="button" :class="['min-h-11 border-b-2 px-1 text-sm font-medium transition-colors', activeTab === tab.id ? 'border-accent text-accent' : 'border-transparent text-ink-3 hover:text-ink']" @click="activeTab = tab.id as 'books' | 'authors'; search = ''">{{ tab.label }}</button></div>
      <BaseButton class="mb-3 w-full sm:w-auto" @click="activeTab === 'books' ? openCreateBook() : openCreateAuthor()">＋ Nuevo {{ activeTab === 'books' ? 'libro' : 'autor' }}</BaseButton>
    </div>
    <label class="relative mb-5 block max-w-md"><span class="sr-only">Buscar registros</span><input v-model="search" type="search" :placeholder="activeTab === 'books' ? 'Buscar libro, autor o género…' : 'Buscar autor o país…'" class="min-h-11 w-full rounded-md border border-rule bg-paper pl-10 pr-4 text-sm text-ink focus:border-accent focus:outline-none"><svg class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg></label>

    <div v-if="loading" class="space-y-3"><div v-for="n in 6" :key="n" class="skeleton h-16 rounded-lg" /></div>
    <ContentState v-else-if="activeTab === 'books' && !filteredBooks.length" title="No hay libros para mostrar" description="Añade una obra o cambia el término de búsqueda." />
    <ContentState v-else-if="activeTab === 'authors' && !filteredAuthors.length" title="No hay autores para mostrar" description="Añade un autor o cambia el término de búsqueda." />

    <template v-else-if="activeTab === 'books'">
      <BaseCard variant="outlined" padding="none" class="hidden overflow-hidden md:block"><div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="border-b border-rule bg-paper-2/60"><th class="px-5 py-3 text-left font-medium text-ink-3">Título</th><th class="px-5 py-3 text-left font-medium text-ink-3">Autor</th><th class="px-5 py-3 text-left font-medium text-ink-3">Año</th><th class="px-5 py-3 text-left font-medium text-ink-3">Género</th><th class="px-5 py-3 text-right font-medium text-ink-3">Acciones</th></tr></thead><tbody><tr v-for="book in filteredBooks" :key="book.id" class="border-b border-rule/60 hover:bg-paper-2/40"><td class="px-5 py-4 font-medium text-ink">{{ book.title }}</td><td class="px-5 py-4 text-ink-2">{{ authorName(book.author_id) }}</td><td class="px-5 py-4 font-[var(--font-mono)] text-ink-2">{{ book.publication_year }}</td><td class="px-5 py-4 text-ink-2">{{ book.genre }}</td><td class="px-5 py-3"><div class="flex justify-end gap-1"><BaseButton variant="ghost" size="sm" @click="openEditBook(book)">Editar</BaseButton><BaseButton variant="ghost" size="sm" class="text-danger" @click="deleteTarget = { kind: 'book', id: book.id, label: book.title }">Eliminar</BaseButton></div></td></tr></tbody></table></div></BaseCard>
      <div class="grid gap-3 md:hidden"><article v-for="book in filteredBooks" :key="book.id" class="rounded-lg border border-rule bg-paper-2/35 p-4"><div class="flex items-start justify-between gap-3"><div class="min-w-0"><p class="truncate font-medium text-ink">{{ book.title }}</p><p class="mt-1 truncate text-sm text-ink-3">{{ authorName(book.author_id) }}</p></div><span class="rounded-full bg-accent/10 px-2.5 py-1 font-[var(--font-mono)] text-xs text-accent">{{ book.publication_year }}</span></div><p class="mt-3 text-xs text-ink-3">{{ book.genre }} · {{ book.country }}</p><div class="mt-3 flex gap-2 border-t border-rule pt-3"><BaseButton variant="secondary" size="sm" class="flex-1" @click="openEditBook(book)">Editar</BaseButton><BaseButton variant="ghost" size="sm" class="text-danger" @click="deleteTarget = { kind: 'book', id: book.id, label: book.title }">Eliminar</BaseButton></div></article></div>
    </template>

    <template v-else>
      <BaseCard variant="outlined" padding="none" class="hidden overflow-hidden md:block"><table class="w-full text-sm"><thead><tr class="border-b border-rule bg-paper-2/60"><th class="px-5 py-3 text-left font-medium text-ink-3">Nombre</th><th class="px-5 py-3 text-left font-medium text-ink-3">País</th><th class="px-5 py-3 text-left font-medium text-ink-3">Periodo</th><th class="px-5 py-3 text-right font-medium text-ink-3">Acciones</th></tr></thead><tbody><tr v-for="author in filteredAuthors" :key="author.id" class="border-b border-rule/60 hover:bg-paper-2/40"><td class="px-5 py-4 font-medium text-ink">{{ author.name }}</td><td class="px-5 py-4 text-ink-2">{{ author.country }}</td><td class="px-5 py-4 font-[var(--font-mono)] text-ink-2">{{ author.birth_year }}–{{ author.death_year || 'presente' }}</td><td class="px-5 py-3"><div class="flex justify-end gap-1"><BaseButton variant="ghost" size="sm" @click="openEditAuthor(author)">Editar</BaseButton><BaseButton variant="ghost" size="sm" class="text-danger" @click="deleteTarget = { kind: 'author', id: author.id, label: author.name }">Eliminar</BaseButton></div></td></tr></tbody></table></BaseCard>
      <div class="grid gap-3 md:hidden"><article v-for="author in filteredAuthors" :key="author.id" class="rounded-lg border border-rule bg-paper-2/35 p-4"><div><p class="font-medium text-ink">{{ author.name }}</p><p class="mt-1 text-sm text-ink-3">{{ author.country }} · {{ author.birth_year }}–{{ author.death_year || 'presente' }}</p></div><div class="mt-3 flex gap-2 border-t border-rule pt-3"><BaseButton variant="secondary" size="sm" class="flex-1" @click="openEditAuthor(author)">Editar</BaseButton><BaseButton variant="ghost" size="sm" class="text-danger" @click="deleteTarget = { kind: 'author', id: author.id, label: author.name }">Eliminar</BaseButton></div></article></div>
    </template>

    <BaseModal :open="showBookModal" :title="editingBook ? 'Editar libro' : 'Nuevo libro'" max-width="lg" @close="showBookModal = false"><form class="grid gap-4" @submit.prevent="saveBook"><BaseInput v-model="bookForm.title" label="Título" required/><div class="grid gap-4 sm:grid-cols-2"><label class="flex flex-col gap-1.5 text-sm font-medium text-ink-2">Autor<select v-model="bookForm.author_id" required class="min-h-11 rounded-md border border-rule bg-paper px-4 text-sm text-ink focus:border-accent focus:outline-none"><option v-for="author in authors" :key="author.id" :value="author.id">{{ author.name }}</option></select></label><BaseInput v-model="bookForm.country" label="País" required/></div><div class="grid gap-4 sm:grid-cols-2"><BaseInput v-model.number="bookForm.publication_year" label="Año de publicación" type="number" required/><BaseInput v-model="bookForm.genre" label="Género" required/></div><BaseInput v-model="bookForm.cover_url" label="URL de portada" placeholder="https://…"/><div v-if="previewEdition || bookForm.cover_url" class="rounded-lg border border-rule bg-paper-2/50 p-4"><p class="mb-3 text-xs font-semibold uppercase tracking-wider text-ink-3">Vista previa</p><div class="mx-auto w-28"><EditorialCover v-if="previewEdition" :edition="previewEdition" sizes="112px"/><img v-else-if="bookForm.cover_url" :src="bookForm.cover_url" alt="Vista previa de portada" class="aspect-[2/3] w-full rounded-md object-contain" /></div><p v-if="previewEdition" class="mt-3 text-center text-xs text-ink-3">Portada vinculada automáticamente por título</p></div><label class="flex flex-col gap-1.5 text-sm font-medium text-ink-2">Descripción<textarea v-model="bookForm.description" rows="4" class="rounded-md border border-rule bg-paper px-4 py-3 text-ink focus:border-accent focus:outline-none" /></label><div class="mt-2 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end"><BaseButton variant="ghost" type="button" @click="showBookModal = false">Cancelar</BaseButton><BaseButton type="submit" :loading="saving">{{ editingBook ? 'Guardar cambios' : 'Crear libro' }}</BaseButton></div></form></BaseModal>
    <BaseModal :open="showAuthorModal" :title="editingAuthor ? 'Editar autor' : 'Nuevo autor'" max-width="lg" @close="showAuthorModal = false"><form class="grid gap-4" @submit.prevent="saveAuthor"><BaseInput v-model="authorForm.name" label="Nombre" required/><BaseInput v-model="authorForm.country" label="País" required/><div class="grid gap-4 sm:grid-cols-2"><BaseInput v-model.number="authorForm.birth_year" label="Año de nacimiento" type="number" required/><BaseInput v-model.number="authorForm.death_year" label="Año de fallecimiento" type="number"/></div><BaseInput v-model="authorForm.image_url" label="URL de imagen" placeholder="https://…"/><label class="flex flex-col gap-1.5 text-sm font-medium text-ink-2">Biografía<textarea v-model="authorForm.biography" rows="4" class="rounded-md border border-rule bg-paper px-4 py-3 text-ink focus:border-accent focus:outline-none" /></label><div class="mt-2 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end"><BaseButton variant="ghost" type="button" @click="showAuthorModal = false">Cancelar</BaseButton><BaseButton type="submit" :loading="saving">{{ editingAuthor ? 'Guardar cambios' : 'Crear autor' }}</BaseButton></div></form></BaseModal>
    <BaseModal :open="Boolean(deleteTarget)" title="Confirmar eliminación" max-width="sm" @close="deleteTarget = null"><p class="text-ink-2">Vas a eliminar <strong class="font-medium text-ink">{{ deleteTarget?.label }}</strong>. Esta acción no se puede deshacer.</p><div class="mt-6 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end"><BaseButton variant="ghost" @click="deleteTarget = null">Cancelar</BaseButton><BaseButton variant="danger" :loading="saving" @click="confirmDelete">Eliminar definitivamente</BaseButton></div></BaseModal>
  </div>
</template>
