import Vue from 'vue'
import Router from 'vue-router'
import store from "@/store";
import TheMainWrapper from "@/components/TheMainWrapper";
import TheArticleView from "@/components/TheArticleView";
import TheFrontView from "@/components/TheFrontView";
import TheTaskHandler from "@/components/TheTaskHandler";
import TheProfileView from "@/components/TheProfileView";
import TheListAllView from "@/components/TheListAllView";

Vue.use(Router)

const router = new Router({
  mode: 'history',
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { x:0, y:0 }
    }
  },
  routes: [
    {
      path: '/',

      components: {
          main: TheMainWrapper,
      },

      meta: {
        title: 'MeMo - Home',
        metaTags: [
          { name: 'description', content: 'MeMo app from Thrive' },
          { name: 'og:description', content: 'MeMo app from Thrive' }
          ]
      },

      children: [
        {
          path: 'home',
          component: TheFrontView,
          meta: {
            title: 'MeMo - This Week',
            KeepAlive: true,
            metaTags: [
              { name: 'description', content: 'Your tasks for this week' },
              { name: 'og:description', content: 'Your tasks for this week' }
            ]
          }
        },
        {
          path: 'article',
          component: TheArticleView,
          meta: {
            title: 'MeMo - Article',
            KeepAlive: false
          },
          beforeEnter: (to, from, next) => {
            if (store.getters.getTask === '') {
              next('home')
            } else {
              next()
            }
          }
        },
        {
          path: 'task',
          component: TheTaskHandler,
          meta: {
            title: 'MeMo - Task',
            KeepAlive: false
          },
          beforeEnter: (to, from, next) => {
            if (store.getters.getTask === '') {
              next('home')
            } else {
              next()
            }
          }
        },
        {
          path: 'profile',
          component: TheProfileView,
          meta: {
            title: 'MeMo - Profile',
            KeepAlive: false,
            metaTags: [
              { name: 'description', content: 'Your profile information' },
              { name: 'og:description', content: 'Your profile information' }
            ]
          }
        },
        {
          path: 'channel',
          component: TheListAllView,
          meta: {
            title: 'MeMo - All Content',
            KeepAlive: false
          }
        }
      ]
    }
  ]
})
  router.beforeEach((to, from, next) => {
    const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title)
    const nearestWithMeta = to.matched.slice().reverse().find(r => r.meta && r.meta.metaTags)
    const previousNearestWithMeta = from.matched.slice().reverse().find(r => r.meta && r.meta.metaTags)

    if(nearestWithTitle) {
      document.title = nearestWithTitle.meta.title
    } else if (nearestWithMeta) {
      document.title = previousNearestWithMeta.meta.title
    }

    Array.from(document.querySelectorAll('[data-vue-router-controlled]')).map(el => el.parentNode.removeChild(el))

    if(!nearestWithMeta) return next()

    nearestWithMeta.meta.metaTags.map(tagDef => {
      const tag = document.createElement('meta')
      Object.keys(tagDef).forEach(key => {
        tag.setAttribute(key, tagDef[key])
      })
      tag.setAttribute('data-vue-router-controlled', '')
      return tag
    }).forEach(tag => document.head.appendChild(tag))

    next()
  })

export default router;