import { api } from '@/services/api'
import type { Narudzba, NarudzbaKreiranje, StatusNarudzbe } from '@/types/narudzba'

export async function kreirajNarudzbu(tijelo: NarudzbaKreiranje): Promise<Narudzba> {
  const { data } = await api.post<Narudzba>('/orders/', tijelo)
  return data
}

export async function dohvatiMojeNarudzbe(): Promise<Narudzba[]> {
  const { data } = await api.get<Narudzba[]>('/orders/my')
  return data
}

export async function dohvatiNarudzbu(id: number): Promise<Narudzba> {
  const { data } = await api.get<Narudzba>(`/orders/${id}`)
  return data
}

export async function promijeniStatus(id: number, noviStatus: StatusNarudzbe): Promise<Narudzba> {
  const { data } = await api.patch<Narudzba>(
    `/orders/${id}/status`,
    null,
    { params: { new_status: noviStatus } },
  )
  return data
}
