import DashboardLayout from '../layout/DashboardLayout.vue'
import NotFound from '../pages/NotFoundPage.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import { isAuthenticated } from '@/components/services/auth'; // Importa la función de autenticación

// Admin pages
import Overview from 'src/pages/Overview.vue'
import UserProfile from 'src/pages/UserProfile.vue'
import TableList from 'src/pages/TableList.vue'
import Typography from 'src/pages/Typography.vue'
import Icons from 'src/pages/Icons.vue'
import Maps from 'src/pages/Maps.vue'
import Notifications from 'src/pages/Notifications.vue'
import Upgrade from 'src/pages/Upgrade.vue'

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/admin/overview'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/admin',
    component: DashboardLayout,
    redirect: '/admin/overview',
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: Overview,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login'); // Redirige a login si no está autenticado
          }
        }
      },
      {
        path: 'user',
        name: 'User',
        component: UserProfile,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'table-list',
        name: 'Table List',
        component: TableList,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'typography',
        name: 'Typography',
        component: Typography,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'icons',
        name: 'Icons',
        component: Icons,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'maps',
        name: 'Maps',
        component: Maps,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: Notifications,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      },
      {
        path: 'upgrade',
        name: 'Upgrade to PRO',
        component: Upgrade,
        beforeEnter: (to, from, next) => {
          if (isAuthenticated()) {
            next();
          } else {
            next('/login');
          }
        }
      }
    ]
  },
  { path: '*', component: NotFound }
]

export default routes
