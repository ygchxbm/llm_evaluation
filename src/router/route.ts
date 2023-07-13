import { RouteRecordRaw } from 'vue-router';

export const constantRoutes: Array<RouteRecordRaw> = [
	{
		path: '/',
		name: '/',
		component: () => import('@/layout/index.vue'),
		redirect: '/npc/all',
		meta: {
			title: '首页'
		},
		children: [
			{
				path: '/:path(.*)*',
				name: 'notFound',
				component: () => import('@/views/error/404.vue'),
				meta: {
					title: 'message.staticRoutes.notFound',
					isHide: true,
				},
			},
			{
				path: '/401',
				name: 'noPower',
				// component: () => import('@/views/index/index.vue'),
				component: () => import('@/views/error/401.vue'),
				meta: {
					title: 'message.staticRoutes.noPower',
					isHide: true,
				},
			},
			{
				path: 'questionnaire',
				// name: 'noPower',
				component: () => import('@/views/index/questionnaire.vue'),
				// component: () => import('@/views/error/401.vue'),
				meta: {
					title: 'message.staticRoutes.noPower',
					isHide: true,
				},
			},
			{
				path: 'transit',
				name: '发起评测',
				component: () => import('@/views/index/transit.vue'),
				meta: {
					title: 'message.staticRoutes.noPower',
					isHide: true,
				},
			},
			{
				path: 'llm/:sid?',
				name: '大语言模型评测',
				component: () => import('@/views/index/index.vue'),
				meta: {
					title: '大语言模型评测',
					// roles: ['user'],
					// icon: 'DataBoard',
					isHide: true,
				},
			},
		],
		
	},
	{
		path: '/answering',
		name: '评测中',
		component: () => import('@/views/index/answering.vue'),
		meta: {
			title: '评测中',
			isHide: true,
		},
	},
	{
		path: '/evaluatedPage',
		name: '评测完成',
		component: () => import('@/views/index/evaluatedPage.vue'),
		meta: {
			title: '评测完成',
			isHide: true,
		},
	},

];
