export interface StavkaJelovnika {
  id: number
  name: string
  description: string | null
  price: number
  is_available: boolean
  restaurant_id: number
}

export interface StavkaKreiranje {
  name: string
  description?: string
  price: number
  is_available: boolean
  restaurant_id: number
}
