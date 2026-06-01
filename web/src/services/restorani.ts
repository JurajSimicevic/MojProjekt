import { api } from '@/services/api'
import type { Restoran, RestoranKreiranje } from '@/types/restoran'

export async function dohvatiRestorante(): Promise<Restoran[]> {
  const { data } = await api.get<Restoran[]>('/restaurants/')
  return data
}

export async function dohvatiRestoran(id: number): Promise<Restoran> {
  const { data } = await api.get<Restoran>(`/restaurants/${id}`)
  return data
}

export async function kreirajRestoran(tijelo: RestoranKreiranje): Promise<Restoran> {
  const { data } = await api.post<Restoran>('/restaurants/', tijelo)
  return data
}
