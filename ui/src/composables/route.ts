import { RouteRecordRaw } from 'vue-router';



const knowl_routes_config = [
  {
    path: '/knowl', 
    name: 'knowl_index', 
    component:() => import('@/views/knowl/knowl_index.vue')
  },
]



const routes: Array<RouteRecordRaw> = [
  {
    path: '/', 
    name: 'index', 
    component: () => import('@/views/Index.vue'),
    children: [
      { path: '/', name:'home', component: () => import('@/views/Home.vue') }, 
      {
        path: 'knowl', 
        name: 'knowl', 
        component: ()=> import('@/views/knowl/knowl_index.vue'), 
        children: knowl_routes_config
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue')
  }
];






export default routes;