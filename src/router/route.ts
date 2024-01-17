import { RouteRecordRaw } from 'vue-router';

export const constantRoutes: Array<RouteRecordRaw> = [
	{
		path: '/',
		name: '/',
		component: () => import('@/layout/index.vue'),
		redirect: '/Login',
		meta: {
			title: '首页',
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
				path: '/home',
				name: 'Home',
				component: () => import('@/views/home/index.vue'),
				meta: {
					title: "首页",
				}
			},
			{
				path: '/initiateEvaluation',
				name: 'InitiateEvaluation',
				component: () => import('@/views/initiateEvaluation/index.vue'),
				meta: {
					title: "发起评测",
				}
			},
			{
				path: '/myAssessment',
				name: 'MyAssessment',
				component: () => import('@/views/myAssessment/index.vue'),
				meta: {
					title: "我的测评",
				}
			},
			{
				path: '/modeComparison',
				name: 'ModeComparison',
				component: () => import('@/views/modeComparison/index.vue'),
				meta: {
					title: "模型对比",
					isHide:true,
				}
			},
			{
				path: '/questionBankManagement',
				name: 'QuestionBankManagement',
				component: () => import('@/views/questionBankManagement/index.vue'),
				meta: {
					title: "题库管理",
				}
			},
			// {
			// 	path: '/test',
			// 	name: 'test',
			// 	component: () => import('@/views/test/index.vue'),
			// 	meta: {
			// 		title: "测试",
			// 	}
			// },
		],
	},
	{
		path: '/evaluateDetail',
		name: 'EvaluateDetail',
		component: () => import('@/views/evaluateDetail/index.vue'),
		meta: {
			title: "评测详情",
			isHide:true,
		}
	},
	{
		path: '/evaluateEnd',
		name: 'EvaluateEnd',
		component: () => import('@/views/evaluateEnd/index.vue'),
		meta: {
			title: "评测结束",
			isHide:true,
		}
	},
	{
		path: '/Login',
		name: 'Login',
		component: () => import('@/views/test/index.vue'),
		meta: {
			title: "登录",
			isHide:true,
		}
	}

	//
	// {
	// 	path: '/answering',
	// 	name: '评测中',
	// 	component: () => import('@/views/index/answering.vue'),
	// 	meta: {
	// 		title: '评测中',
	// 		isHide: true,
	// 	},
	// },
	// {
	// 	path: '/evaluatedPage',
	// 	name: '评测完成',
	// 	component: () => import('@/views/index/evaluatedPage.vue'),
	// 	meta: {
	// 		title: '评测完成',
	// 		isHide: true,
	// 	},
	// },



];
