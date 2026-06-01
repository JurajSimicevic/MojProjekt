export type StatusNarudzbe =
  | 'pending'
  | 'accepted'
  | 'preparing'
  | 'ready'
  | 'on_the_way'
  | 'delivered'
  | 'cancelled'

export interface StavkaNarudzbe {
  id: number
  menu_item_id: number
  item_name: string
  price_at_purchase: number
}

export interface Narudzba {
  id: number
  customer_id: number
  restaurant_id: number
  courier_id: number | null
  total_price: number
  status: StatusNarudzbe
  created_at: string
  items: StavkaNarudzbe[]
}

export interface NarudzbaKreiranje {
  restaurant_id: number
  item_ids: number[]
}
