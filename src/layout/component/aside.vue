<template>
	<div class="h100" v-show="!isTagsViewCurrenFull">
		<el-aside class="layout-aside" :class="setCollapseStyle">
			<Logo />
			<el-scrollbar class="flex-auto up-part-menu" ref="layoutAsideScrollbarRef" @mouseenter="onAsideEnterLeave(true)" @mouseleave="onAsideEnterLeave(false)">
				<Vertical :menuList="menuList" />
			</el-scrollbar>
			<div class="foot" @click="showSetting"><el-icon style="margin-right: 6px;"><Warning /></el-icon>Game Profile</div>
		</el-aside>

		<el-dialog width="80%" style="max-width: 100%" v-model="settingVisible" title="Game Profile" :close-on-click-modal="false">
			<el-form :model="setting" label-width="130px">
				<el-form-item label="Personality Data">
					<el-input v-model="setting.personality_data" type="textarea" />
				</el-form-item>
				<el-form-item label="World Base Knowledge">
					<el-input v-model="setting.world_base_knowledge" type="textarea" />
				</el-form-item>
				<el-form-item label="Location Knowledge">
					<el-input v-model="setting.location_knowledge" type="textarea" />
				</el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button type="primary" @click="handleSaveSetting" :loading="settingSaving">Submit</el-button>
				</span>
			</template>
		</el-dialog>

	</div>
</template>

<script lang="ts">
import { toRefs, reactive, computed, watch, getCurrentInstance, onBeforeMount, defineComponent } from 'vue';
import { storeToRefs } from 'pinia';
import pinia from '@/stores/index';
import { useRoutesList } from '@/stores/routesList';
import { useThemeConfig } from '@/stores/themeConfig';
import { useTagsViewRoutes } from '@/stores/tagsViewRoutes';
import Logo from '@/layout/logo/index.vue';
import Vertical from '@/layout/navMenu/vertical.vue';
import { constantRoutes } from '@/router/route';
import { RouteRecordRaw } from 'vue-router';
import { MenuItem } from '@/stores/interface';
import { npcList, getSetting, saveSetting } from '@/api';
import { ElMessage, ElMessageBox } from 'element-plus';
import router from '../../router';
import { Warning, Menu } from '@element-plus/icons-vue';

export default defineComponent({
	name: 'layoutAside',
	components: { Logo, Vertical, Warning, Menu },
	setup() {
		const { proxy } = <any>getCurrentInstance();
		const stores = useRoutesList();
		const storesThemeConfig = useThemeConfig();
		const storesTagsViewRoutes = useTagsViewRoutes();
		const { themeConfig } = storeToRefs(storesThemeConfig);
		const { isTagsViewCurrenFull } = storeToRefs(storesTagsViewRoutes);
		const state = reactive({
			menuList: [
				{
					path: '/npc/all',
					meta: { title: 'Show All' },
				},
				{
					path: '/npc/tree',
					meta: { title: 'Character Tree' },
					children: [],
				},
			] as MenuItem[],
			clientWidth: 0,
			settingVisible: false,
			setting: {
				personality_data: '',
				world_base_knowledge: '',
				location_knowledge: '',
			},
			settingSaving: false,
		});
		// 设置菜单展开/收起时的宽度
		const setCollapseStyle = computed(() => {
			const { layout, isCollapse, menuBar } = themeConfig.value;
			const asideBrTheme = ['#FFFFFF', '#FFF', '#fff', '#ffffff'];
			const asideBrColor = asideBrTheme.includes(menuBar) ? 'layout-el-aside-br-color' : '';
			// 判断是否是手机端
			if (state.clientWidth <= 1000) {
				if (isCollapse) {
					document.body.setAttribute('class', 'el-popup-parent--hidden');
					const asideEle = document.querySelector('.layout-container') as HTMLElement;
					const modeDivs = document.createElement('div');
					modeDivs.setAttribute('class', 'layout-aside-mobile-mode');
					asideEle.appendChild(modeDivs);
					modeDivs.addEventListener('click', closeLayoutAsideMobileMode);
					return [asideBrColor, 'layout-aside-mobile', 'layout-aside-mobile-open'];
				} else {
					// 关闭弹窗
					closeLayoutAsideMobileMode();
					return [asideBrColor, 'layout-aside-mobile', 'layout-aside-mobile-close'];
				}
			} else {
				if (layout === 'columns') {
					// 分栏布局，菜单收起时宽度给 1px
					if (isCollapse) return [asideBrColor, 'layout-aside-pc-1'];
					else return [asideBrColor, 'layout-aside-pc-220'];
				} else {
					// 其它布局给 64px
					if (isCollapse) return [asideBrColor, 'layout-aside-pc-64'];
					else return [asideBrColor, 'layout-aside-pc-220'];
				}
			}
		});
		// 关闭移动端蒙版
		const closeLayoutAsideMobileMode = () => {
			const el = document.querySelector('.layout-aside-mobile-mode');
			el?.setAttribute('style', 'animation: error-img-two 0.3s');
			setTimeout(() => {
				el?.parentNode?.removeChild(el);
			}, 300);
			const clientWidth = document.body.clientWidth;
			if (clientWidth < 1000) themeConfig.value.isCollapse = false;
			document.body.setAttribute('class', '');
		};
		// 设置显示/隐藏 logo
		const setShowLogo = computed(() => {
			let { layout, isShowLogo } = themeConfig.value;
			return (isShowLogo && layout === 'defaults') || (isShowLogo && layout === 'columns');
		});
		// 设置/过滤路由（非静态路由/是否显示在菜单中）
		const setFilterRoutes = () => {
			if (themeConfig.value.layout === 'columns') return false;
			if(constantRoutes[0] && constantRoutes[0].children && constantRoutes.length >= 1) {
				// state.menuList = filterRoutesFun(constantRoutes[0].children.concat(constantRoutes.slice(1)));
			}
		};
		// 路由过滤递归函数
		const filterRoutesFun = (arr: Array<RouteRecordRaw>) => {
			return arr
				.filter((item: RouteRecordRaw) => !item.meta || !item.meta.isHide)
				.map((item: RouteRecordRaw) => {
					const { meta } = item;
					const nitem: MenuItem = {
						path: item.path,
						meta: {
							title: meta && meta.title ? `${meta.title}` : item.path,
							icon: meta && meta.icon ? `${meta.icon}` : '',
							isLink: meta && meta.isLink ? !!meta.isLink : false,
							isIframe: meta && meta.isIframe ? !!meta.isIframe : false,
						},
					};
					if (item.children) {
						nitem.children = filterRoutesFun(item.children);
					}
					return nitem;
				});
		};
		// 设置菜单导航是否固定（移动端）
		const initMenuFixed = (clientWidth: number) => {
			state.clientWidth = clientWidth;
		};
		// 鼠标移入、移出
		const onAsideEnterLeave = (bool: Boolean) => {
			let { layout } = themeConfig.value;
			if (layout !== 'columns') return false;
			if (!bool) proxy.mittBus.emit('restoreDefault');
			stores.setColumnsMenuHover(bool);
		};
		// 监听 themeConfig 配置文件的变化，更新菜单 el-scrollbar 的高度
		watch(themeConfig.value, (val) => {
			if (val.isShowLogoChange !== val.isShowLogo) {
				if (!proxy.$refs.layoutAsideScrollbarRef) return false;
				proxy.$refs.layoutAsideScrollbarRef.update();
			}
		});
		// 监听vuex值的变化，动态赋值给菜单中
		watch(
			pinia.state,
			(val) => {
				let { layout, isClassicSplitMenu } = val.themeConfig.themeConfig;
				if (layout === 'classic' && isClassicSplitMenu) return false;
				setFilterRoutes();
			},
			{
				deep: true,
			}
		);
		// 页面加载前
		onBeforeMount(() => {
			initMenuFixed(document.body.clientWidth);
			setFilterRoutes();
			// 此界面不需要取消监听(proxy.mittBus.off('setSendColumnsChildren))
			// 因为切换布局时有的监听需要使用，取消了监听，某些操作将不生效
			proxy.mittBus.on('setSendColumnsChildren', (res: any) => {
				state.menuList = res.children;
			});
			proxy.mittBus.on('setSendClassicChildren', (res: any) => {
				let { layout, isClassicSplitMenu } = themeConfig.value;
				if (layout === 'classic' && isClassicSplitMenu) {
					state.menuList = [];
					state.menuList = res.children;
				}
			});
			proxy.mittBus.on('getBreadcrumbIndexSetFilterRoutes', () => {
				setFilterRoutes();
			});
			proxy.mittBus.on('layoutMobileResize', (res: any) => {
				initMenuFixed(res.clientWidth);
				closeLayoutAsideMobileMode();
			});
		});
		
		function loadNpcs() {
			npcList().then((npcs) => {
				const menus: MenuItem[] = [];
				const hash = {};
				npcs.forEach(x => hash[x.id] = {
					path: `/npc/${x.id}`,
					children: [],
					meta: {
						id: x.id,
						title: x.name,
					},
				});
				npcs.forEach(x => {
					if(+x.parent_id === 0) {
						menus.push(hash[x.id])
					} else if(hash[x.parent_id]) {
						hash[x.parent_id].children.push(hash[x.id]);
					} else {
						console.error('not found npc', x.parent_id);
					}
				});
				state.menuList[1].children = menus;
			});
		}

		function loadSetting() {
			getSetting().then(res => state.setting = res);
		}

		function handleSaveSetting() {
			state.settingSaving = true;
			saveSetting(state.setting).then(() => {
				state.settingSaving = false;
				state.settingVisible = false;
				ElMessage.success('Save Success');
			}).catch(e => {
				state.settingSaving = false;
				ElMessageBox.alert(`${e}`);
				console.error('saveSetting', e);
			})
		}

		loadNpcs();
		loadSetting();

		return {
			setCollapseStyle,
			setShowLogo,
			isTagsViewCurrenFull,
			onAsideEnterLeave,
			showSetting() {
				state.settingVisible = true;
			},
			handleSaveSetting,
			...toRefs(state),
		};
	},
});
</script>

<style lang="scss" scoped>
	.layout-aside {
		background: url('@/assets/bg.png');
		background-size: 100% auto;
	}
	.foot {
		opacity: 0.7;
		color: #fff;
		font-size: 18px;
		padding: 30px 0;
		text-align: center;
		cursor: pointer;
	}
	.ps-dialog {
		line-height: 2;
		padding: 0 20px;
		word-break: break-word;
	}
	.up-part-menu {
		max-height: calc(var(--app-height) - 293px);
	}
	.mcollapse {
		:deep(.el-collapse-item__content) {
			padding: 0 12px 25px 0;
		}
	}
</style>