import { createRouter, createWebHashHistory } from 'vue-router';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import pinia from '@/stores/index';
import { storeToRefs } from 'pinia';
import { useUserInfo } from '@/stores/userInfo';
import { constantRoutes } from '@/router/route';

/**
 * 创建一个可以被 Vue 应用程序使用的路由实例
 * @method createRouter(options: RouterOptions): Router
 * @link 参考：https://next.router.vuejs.org/zh/api/#createrouter
 */
export const router = createRouter({
	history: createWebHashHistory(),
	routes: constantRoutes,
});

NProgress.configure({ showSpinner: false });

const store = useUserInfo(pinia);
const whiteList = ["/","/401", "403", "404","/test","/Login","/home","/initiateEvaluation","/myAssessment","/modeComparison","/questionBankManagement","/evaluateDetail","/evaluateEnd"];

router.beforeEach(async (to, from, next) => {
	NProgress.start();
	if (whiteList.includes(to.path)) {
		next();
		return;
	}
	const { userInfos } = storeToRefs(store);
	// console.log(userInfos.value);
	if (userInfos.value.name) {
		next();
	} else {
		try {
			await useUserInfo(pinia).setUserInfos();
			if (!userInfos.value.permissions.includes('admin') && to.meta && to.meta.roles && !(to.meta.roles as any).some((x: string) => userInfos.value.permissions.includes(x))) {
				next('/403');
			} else {
				next();
			}
		} catch (error) {
			console.error(error);
			next('/401');
			NProgress.done();
		}
	}
});

// 路由加载后
router.afterEach(() => {
	NProgress.done();
});

// 导出路由
export default router;
