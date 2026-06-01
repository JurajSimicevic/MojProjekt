import { api } from '@/services/api'
import type { StavkaJelovnika, StavkaKreiranje } from '@/types/stavka_jelovnika'

export async function dohvatiJelovnik(restaurantId: number): Promise<StavkaJelovnika[]> {
  const { data } = await api.get<StavkaJelovnika[]>(`/menu/restaurants/${restaurantId}/items`)
  return data
}

export async function kreirajStavku(tijelo: StavkaKreiranje): Promise<StavkaJelovnika> {
  const { data } = await api.post<StavkaJelovnika>('/menu/items', tijelo)
  return data
}

export async function promijeniDostupnost(
  itemId: number,
  isAvailable: boolean,
): Promise<StavkaJelovnika> {
  const { data } = await api.patch<StavkaJelovnika>(
    `/menu/items/${itemId}/availability`,
    null,
    { params: { is_available: isAvailable } },
  )
  return data
}
