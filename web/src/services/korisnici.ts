import { api } from '@/services/api'
import type { KorisnikPodaci } from '@/types/korisnik'

export interface KupacRegistracija {
  username: string
  password: string
}

export interface OsobljeKreiranje {
  username: string
  password: string
  role: 'restaurant' | 'courier'
}

export async function registrirajKupca(tijelo: KupacRegistracija): Promise<KorisnikPodaci> {
  const { data } = await api.post<KorisnikPodaci>('/users/register', tijelo)
  return data
}

export async function kreirajOsoblje(tijelo: OsobljeKreiranje): Promise<KorisnikPodaci> {
  const { data } = await api.post<KorisnikPodaci>('/users/staff', tijelo)
  return data
}
