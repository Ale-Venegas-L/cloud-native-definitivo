import veinteSmall from '../assets/img/covers/320/veinte-poemas-de-amor.webp'
import veinteMedium from '../assets/img/covers/640/veinte-poemas-de-amor.webp'
import araucanaSmall from '../assets/img/covers/320/la-araucana.webp'
import araucanaMedium from '../assets/img/covers/640/la-araucana.webp'
import quijoteSmall from '../assets/img/covers/320/don-quijote-1605.webp'
import quijoteMedium from '../assets/img/covers/640/don-quijote-1605.webp'
import canterburySmall from '../assets/img/covers/320/cuentos-de-canterbury.webp'
import canterburyMedium from '../assets/img/covers/640/cuentos-de-canterbury.webp'
import desolacionSmall from '../assets/img/covers/320/desolacion-1922.webp'
import desolacionMedium from '../assets/img/covers/640/desolacion-1922.webp'
import shakespeareSmall from '../assets/img/covers/320/shakespeare-first-folio-1623.webp'
import shakespeareMedium from '../assets/img/covers/640/shakespeare-first-folio-1623.webp'
import sonetosSmall from '../assets/img/covers/320/cien-sonetos-de-amor.webp'
import sonetosMedium from '../assets/img/covers/640/cien-sonetos-de-amor.webp'

export interface EditorialEdition {
  id: string
  title: string
  author: string
  year: string
  kind: 'Facsímil histórico' | 'Edición contemporánea'
  description: string
  small: string
  medium: string
  alt: string
}

export const editorialEditions: EditorialEdition[] = [
  { id: 'don-quijote-1605', title: 'Don Quijote de la Mancha', author: 'Miguel de Cervantes', year: '1605', kind: 'Facsímil histórico', description: 'Portada de la primera edición publicada en Madrid por Juan de la Cuesta.', small: quijoteSmall, medium: quijoteMedium, alt: 'Portada histórica de Don Quijote de la Mancha de 1605' },
  { id: 'la-araucana', title: 'La Araucana', author: 'Alonso de Ercilla', year: '1569', kind: 'Facsímil histórico', description: 'Una portada temprana de la epopeya que relata la guerra de Arauco.', small: araucanaSmall, medium: araucanaMedium, alt: 'Portada histórica de La Araucana' },
  { id: 'shakespeare-first-folio-1623', title: 'First Folio', author: 'William Shakespeare', year: '1623', kind: 'Facsímil histórico', description: 'La primera recopilación de comedias, historias y tragedias de Shakespeare.', small: shakespeareSmall, medium: shakespeareMedium, alt: 'Portada del First Folio de William Shakespeare de 1623' },
  { id: 'desolacion-1922', title: 'Desolación', author: 'Gabriela Mistral', year: '1922', kind: 'Facsímil histórico', description: 'La edición neoyorquina que consolidó la voz poética de Gabriela Mistral.', small: desolacionSmall, medium: desolacionMedium, alt: 'Portada de Desolación de Gabriela Mistral de 1922' },
  { id: 'veinte-poemas-de-amor', title: 'Veinte poemas de amor', author: 'Pablo Neruda', year: '1924', kind: 'Edición contemporánea', description: 'Una interpretación gráfica contemporánea de uno de los poemarios más leídos.', small: veinteSmall, medium: veinteMedium, alt: 'Portada de Veinte poemas de amor de Pablo Neruda' },
  { id: 'cien-sonetos-de-amor', title: 'Cien sonetos de amor', author: 'Pablo Neruda', year: '1959', kind: 'Edición contemporánea', description: 'Diseño tipográfico y cromático para la colección de sonetos de Neruda.', small: sonetosSmall, medium: sonetosMedium, alt: 'Portada de Cien sonetos de amor de Pablo Neruda' },
  { id: 'cuentos-de-canterbury', title: 'Cuentos de Canterbury', author: 'Geoffrey Chaucer', year: 'c. 1400', kind: 'Edición contemporánea', description: 'Una edición ilustrada que reúne a los peregrinos de la obra de Chaucer.', small: canterburySmall, medium: canterburyMedium, alt: 'Portada ilustrada de Cuentos de Canterbury' }
]

const bookEditionIds: Record<string, string> = {
  'don quijote de la mancha': 'don-quijote-1605',
  hamlet: 'shakespeare-first-folio-1623',
  'romeo y julieta': 'shakespeare-first-folio-1623',
  'la araucana': 'la-araucana',
  desolacion: 'desolacion-1922',
  'veinte poemas de amor': 'veinte-poemas-de-amor',
  'cien sonetos de amor': 'cien-sonetos-de-amor',
  'cuentos de canterbury': 'cuentos-de-canterbury'
}

function normalize(value: string): string {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('es').trim()
}

export function editionForBook(title: string): EditorialEdition | undefined {
  const editionId = bookEditionIds[normalize(title)]
  return editorialEditions.find(edition => edition.id === editionId)
}

export function editionsForAuthor(author: string): EditorialEdition[] {
  return editorialEditions.filter(edition => normalize(edition.author) === normalize(author))
}
