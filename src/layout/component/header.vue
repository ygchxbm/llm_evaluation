<template>
	<el-header class="layout-header">
		<div class="layout-navbars-container">
			<div class="layout-navbars-breadcrumb-index">
				<Breadcrumb />
				<div class="title">{{themeConfig.globalTitle}}</div>
			</div>
		</div>
	</el-header>
</template>

<script lang="ts">

import { defineComponent, ref, computed, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessageBox, ElMessage } from 'element-plus';
import screenfull from 'screenfull';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { useUserInfo } from '@/stores/userInfo';
import { useThemeConfig } from '@/stores/themeConfig';
import other from '@/utils/other';
import { Session, Local } from '@/utils/storage';
import Breadcrumb from './breadcrumb.vue';

export default defineComponent({
	components: { Breadcrumb },
	setup() {
		// 定义变量内容
		const { locale, t } = useI18n();
		const router = useRouter();
		const stores = useUserInfo();
		const storesThemeConfig = useThemeConfig();
		const { userInfos } = storeToRefs(stores);
		const { themeConfig } = storeToRefs(storesThemeConfig);
		const searchRef = ref();
		const state = reactive({
			isScreenfull: false,
			disabledI18n: 'zh-cn',
			disabledSize: 'large',
		});

		// 设置分割样式
		const layoutUserFlexNum = computed(() => {
			let num: string | number = '';
			const { layout, isClassicSplitMenu } = themeConfig.value;
			const layoutArr: string[] = ['defaults', 'columns'];
			if (layoutArr.includes(layout) || (layout === 'classic' && !isClassicSplitMenu)) num = '1';
			else num = '';
			return num;
		});
		// 全屏点击时
		const onScreenfullClick = () => {
			if (!screenfull.isEnabled) {
				ElMessage.warning('暂不不支持全屏');
				return false;
			}
			screenfull.toggle();
			screenfull.on('change', () => {
				if (screenfull.isFullscreen) state.isScreenfull = true;
				else state.isScreenfull = false;
			});
		};
		// 下拉菜单点击时
		const onHandleCommandClick = (path: string) => {
			if (path === 'logOut') {
				ElMessageBox({
					closeOnClickModal: false,
					closeOnPressEscape: false,
					title: t('message.user.logOutTitle'),
					message: t('message.user.logOutMessage'),
					showCancelButton: true,
					confirmButtonText: t('message.user.logOutConfirm'),
					cancelButtonText: t('message.user.logOutCancel'),
					buttonSize: 'default',
					beforeClose: (action, instance, done) => {
						if (action === 'confirm') {
							instance.confirmButtonLoading = true;
							instance.confirmButtonText = t('message.user.logOutExit');
							setTimeout(() => {
								done();
								setTimeout(() => {
									instance.confirmButtonLoading = false;
								}, 300);
							}, 700);
						} else {
							done();
						}
					},
				})
					.then(async () => {
						// 清除缓存/token等
						Session.clear();
						// 使用 reload 时，不需要调用 resetRoute() 重置路由
						window.location.reload();
					})
					.catch(() => {});
			} else {
				router.push(path);
			}
		};
		// 菜单搜索点击
		const onSearchClick = () => {
			searchRef.value.openSearch();
		};
		// 组件大小改变
		const onComponentSizeChange = (size: string) => {
			Local.remove('themeConfig');
			themeConfig.value.globalComponentSize = size;
			Local.set('themeConfig', themeConfig.value);
			initI18nOrSize('globalComponentSize', 'disabledSize');
			window.location.reload();
		};
		// 语言切换
		const onLanguageChange = (lang: string) => {
			Local.remove('themeConfig');
			themeConfig.value.globalI18n = lang;
			Local.set('themeConfig', themeConfig.value);
			locale.value = lang;
			other.useTitle();
			initI18nOrSize('globalI18n', 'disabledI18n');
		};
		// 初始化组件大小/i18n
		const initI18nOrSize = (value: string, attr: string) => {
			state[attr] = Local.get('themeConfig')[value];
		};
		// 页面加载时
		onMounted(() => {
			if (Local.get('themeConfig')) {
				initI18nOrSize('globalComponentSize', 'disabledSize');
				initI18nOrSize('globalI18n', 'disabledI18n');
			}
		});
		return { layoutUserFlexNum, onScreenfullClick, onHandleCommandClick, onSearchClick, onComponentSizeChange, onLanguageChange, state, userInfos, themeConfig };
	}
});

</script>

<style scoped lang="scss">
.layout-navbars-container {
	display: flex;
	flex-direction: column;
	width: 100%;
	height: 100%;
}
.layout-navbars-breadcrumb-index {
	height: 50px;
	display: flex;
	align-items: center;
	color: rgb(217,217,227);
	background: rgb(52,53,65);
	border-bottom: 1px solid hsla(0,0%,100%,.2);
}
.layout-header {
	height: auto;
}
.layout-navbars-breadcrumb-user {
	display: flex;
	align-items: center;
	justify-content: flex-end;
	&-link {
		height: 100%;
		display: flex;
		align-items: center;
		white-space: nowrap;
		&-photo {
			width: 25px;
			height: 25px;
			border-radius: 100%;
		}
	}
	&-icon {
		padding: 0 10px;
		cursor: pointer;
		color: var(--next-bg-topBarColor);
		height: 50px;
		line-height: 50px;
		display: flex;
		align-items: center;
		&:hover {
			background: var(--next-color-user-hover);
			i {
				display: inline-block;
				animation: logoAnimation 0.3s ease-in-out;
			}
		}
	}
	:deep(.el-dropdown) {
		color: var(--next-bg-topBarColor);
	}
	:deep(.el-badge) {
		height: 40px;
		line-height: 40px;
		display: flex;
		align-items: center;
	}
	:deep(.el-badge__content.is-fixed) {
		top: 12px;
	}
}
.title {
	position: absolute;
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 70%;
}
</style>