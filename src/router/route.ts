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
				component: () => import('@/views/error/401.vue'),
				meta: {
					title: 'message.staticRoutes.noPower',
					isHide: true,
				},
			},
			{
				path: 'npc/:sid?',
				name: 'NPC',
				component: () => import('@/views/index/index.vue'),
				meta: {
					title: 'NPC',
					roles: ['user'],
					icon: 'DataBoard',
					isHide: true,
				},
			},
		],
	},
];
