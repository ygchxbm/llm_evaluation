<template>
	<el-menu
		router
		:default-active="defaultActive"
		background-color="transparent"
		:collapse="isCollapse"
		:unique-opened="getThemeConfig.isUniqueOpened"
		:collapse-transition="false"
		class="menu"
	>
		<template v-for="val in menuLists">
			<el-sub-menu :index="val.path" v-if="val.children && val.children.length > 0" :key="val.path">
				<template #title>
					<el-icon v-if="val.meta.icon" color="#fff" :size="14">
						<component :is="val.meta.icon" />
					</el-icon>
					<!--<span>{{ $t(val.meta.title) }}</span>-->
					<el-menu-item :index="val.path" style="padding: 0;background: transparent;border: none;">{{ $t(val.meta.title) }}</el-menu-item>
				</template>
				<SubItem :chil="val.children" />
			</el-sub-menu>
			<template v-else>
				<el-menu-item :index="val.path" :key="val.path">
					<el-icon v-if="val.meta.icon" color="#fff" :size="14">
						<component :is="val.meta.icon" />
					</el-icon>
					<template #title v-if="!val.meta.isLink || (val.meta.isLink && val.meta.isIframe)">
						<span>{{ $t(val.meta.title) }}</span>
					</template>
					<template #title v-else>
						<a :href="val.meta.isLink" target="_blank" rel="opener" class="w100">{{ $t(val.meta.title) }}</a>
					</template>
				</el-menu-item>
			</template>
		</template>
	</el-menu>
</template>

<script lang="ts">
import { toRefs, reactive, computed, defineComponent, watch } from 'vue';
import { useRoute, onBeforeRouteUpdate } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '@/stores/themeConfig';
import SubItem from '@/layout/navMenu/subItem.vue';
import { MenuItem } from '@/stores/interface';

export default defineComponent({
	name: 'navMenuVertical',
	components: { SubItem, },
	props: {
		menuList: {
			type: Array,
			default: () => [] as MenuItem[],
		},
	},
	setup(props) {
		const storesThemeConfig = useThemeConfig();
		const { themeConfig } = storeToRefs(storesThemeConfig);
		const route = useRoute();
		const state = reactive({
			// 修复：https://gitee.com/lyt-top/vue-next-admin/issues/I3YX6G
			defaultActive: route.path,
			isCollapse: false,
			menuLists: [] as MenuItem[],
		});
		// 获取布局配置信息
		const getThemeConfig = computed(() => {
			return themeConfig.value;
		});
		// 设置菜单的收起/展开
		watch(themeConfig.value, () => document.body.clientWidth <= 1000 ? (state.isCollapse = false) : (state.isCollapse = themeConfig.value.isCollapse), { immediate: true });
		watch(() => props.menuList, (res) => state.menuLists = res as MenuItem[], { immediate: true });
		// 路由更新时
		onBeforeRouteUpdate((to) => {
			// 修复：https://gitee.com/lyt-top/vue-next-admin/issues/I3YX6G
			state.defaultActive = to.path;
			const clientWidth = document.body.clientWidth;
			if (clientWidth < 1000) themeConfig.value.isCollapse = false;
		});
		return {
			getThemeConfig,
			...toRefs(state),
		};
	},
});
</script>

<style lang='scss' scoped>
.menu {
	border: none;
	:deep(.el-menu-item) {
		color: #fff;
		font-size: 18px;
		.menu-icon {
			margin-right: 15px;
		}
		span {
			color: #fff;
		}
	}
	:deep(.el-sub-menu__title){
		color: #fff;
		font-size: 18px;
	}
	:deep(.el-menu-item.is-active) {
		border-right: 3px solid #00A9CE;
		color: #00A9CE;
		span {
			color: #00A9CE;
		}
		font-weight: 600;
	}
}
</style>