import axios from 'axios';
import { site } from '../config';

// 配置新建一个 axios 实例
const service = axios.create({
	baseURL: import.meta.env.VITE_API_URL as any,
	timeout: 50000,
	headers: { 'Content-Type': 'application/json' },
});

// 添加请求拦截器
service.interceptors.request.use(
	(config) => {
		if(config.url && !config.url.match(/[&?]site=\w+/)) {
			config.url = config.url + (config.url.includes('?') ? '&' : '?') + `site=${site}`;
		}
		return config;
	},
	(error) => {
		// 对请求错误做些什么
		return Promise.reject(error);
	}
);

// 添加响应拦截器
service.interceptors.response.use(
	(response) => {
		return response.data;
	},
	(error) => {
		return Promise.reject(error.response && error.response.data ? error.response.data : error);
	}
);

// 导出 axios 实例
export default service;
