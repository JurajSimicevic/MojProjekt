import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import PrijavaView from '@/views/PrijavaView.vue'
import RegistracijaView from '@/views/RegistracijaView.vue'
import NepoznatoView from '@/views/NepoznatoView.vue'

import AdminPocetnaView from '@/views/admin/AdminPocetnaView.vue'
import AdminRestoraniView from '@/views/admin/AdminRestoraniView.vue'
import AdminOsobljeView from '@/views/admin/AdminOsobljeView.vue'
import AdminNarudzbView from '@/views/admin/AdminNarudzbView.vue'

import RestoranPocetnaView from '@/views/restoran/RestoranPocetnaView.vue'
import RestoranJelovnikView from '@/views/restoran/RestoranJelovnikView.vue'
import JelovnikStavkaFormaView from '@/views/restoran/JelovnikStavkaFormaView.vue'
import RestoranNarudzbView from '@/views/restoran/RestoranNarudzbView.vue'

import DostavljacPocetnaView from '@/views/dostavljac/DostavljacPocetnaView.vue'
import DostavljacDostavView from '@/views/dostavljac/DostavljacDostavView.vue'

import KupacPocetnaView from '@/views/kupac/KupacPocetnaView.vue'
import KupacRestoraniView from '@/views/kupac/KupacRestoraniView.vue'
import KupacRestoranView from '@/views/kupac/KupacRestoranView.vue'
import KupacNarudzbView from '@/views/kupac/KupacNarudzbView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: () => {
        const auth = useAuthStore()
        if (!auth.isAuthenticated) return '/prijava'
        if (auth.isAdmin) return '/admin/pocetna'
        if (auth.isRestoran) return '/restoran/pocetna'
        if (auth.isDostavljac) return '/dostavljac/pocetna'
        return '/kupac/pocetna'
      },
    },
    {
      path: '/prijava',
      component: PrijavaView,
      meta: { layout: 'gost', javno: true },
    },
    {
      path: '/registracija',
      component: RegistracijaView,
      meta: { layout: 'gost', javno: true },
    },
    {
      path: '/admin',
      meta: { layout: 'aplikacija', uloga: 'admin' },
      children: [
        { path: 'pocetna', component: AdminPocetnaView },
        { path: 'restorani', component: AdminRestoraniView },
        { path: 'osoblje', component: AdminOsobljeView },
        { path: 'narudzbe', component: AdminNarudzbView },
      ],
    },
    {
      path: '/restoran',
      meta: { layout: 'aplikacija', uloga: 'restaurant' },
      children: [
        { path: 'pocetna', component: RestoranPocetnaView },
        { path: 'jelovnik', component: RestoranJelovnikView },
        { path: 'jelovnik/nova-stavka', component: JelovnikStavkaFormaView },
        { path: 'narudzbe', component: RestoranNarudzbView },
      ],
    },
    {
      path: '/dostavljac',
      meta: { layout: 'aplikacija', uloga: 'courier' },
      children: [
        { path: 'pocetna', component: DostavljacPocetnaView },
        { path: 'dostave', component: DostavljacDostavView },
      ],
    },
    {
      path: '/kupac',
      meta: { layout: 'aplikacija', uloga: 'customer' },
      children: [
        { path: 'pocetna', component: KupacPocetnaView },
        { path: 'restorani', component: KupacRestoraniView },
        { path: 'restorani/:id', component: KupacRestoranView },
        { path: 'narudzbe', component: KupacNarudzbView },
      ],
    },
    {
      path: '/:catchAll(.*)*',
      component: NepoznatoView,
      meta: { layout: 'gost', javno: true },
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.javno) {
    if (auth.isAuthenticated) {
      if (auth.isAdmin) return '/admin/pocetna'
      if (auth.isRestoran) return '/restoran/pocetna'
      if (auth.isDostavljac) return '/dostavljac/pocetna'
      return '/kupac/pocetna'
    }
    return true
  }

  if (!auth.isAuthenticated) return '/prijava'

  const uloga = to.meta.uloga as string | undefined
  if (uloga && auth.user?.role !== uloga) {
    if (auth.isAdmin) return '/admin/pocetna'
    if (auth.isRestoran) return '/restoran/pocetna'
    if (auth.isDostavljac) return '/dostavljac/pocetna'
    return '/kupac/pocetna'
  }

  return true
})

export default router
