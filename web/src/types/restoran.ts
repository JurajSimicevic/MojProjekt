export interface Restoran {
  id: number
  name: string
  address: string
  is_active: boolean
  owner_id: number
}

export interface RestoranKreiranje {
  name: string
  address: string
  owner_id: number
}
