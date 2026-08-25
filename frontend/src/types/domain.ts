export interface Author {
  id: string
  name: string
  country: string
  birth_year: number
  death_year: number | null
  biography?: string | null
  image_url?: string | null
}

export interface Book {
  id: string
  title: string
  author_id: string
  country: string
  publication_year: number
  genre: string
  description?: string | null
  cover_url?: string | null
}

export type AuthorPayload = Omit<Author, 'id'>
export type BookPayload = Omit<Book, 'id'>
