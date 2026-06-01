export type Uloga = 'customer' | 'restaurant' | 'courier' | 'admin'

export interface KorisnikPodaci {
  id: number
  username: string
  role: Uloga
  is_active: boolean
}
