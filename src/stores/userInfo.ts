import { defineStore } from 'pinia';
import { UserInfosStates } from './interface';
import { Session } from '@/utils/storage';
import request from '@/utils/request';

/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
	state: (): UserInfosStates => ({
		userInfos: {
			avatar: '',
			name: '',
			permissions: [],
			userid: '',
		},
	}),
	actions: {
		async setUserInfos() {
			const user: any = await request('/user.currentUser');
			// 用户信息模拟数据：{ name: 'test', permissions: ['admin'], userid: 'xing', avatar: 'xx' }
			const userInfos = user;
			// 存储用户信息到浏览器缓存
			Session.set('userInfo', userInfos);
			this.userInfos = userInfos;
		}
	},
});
