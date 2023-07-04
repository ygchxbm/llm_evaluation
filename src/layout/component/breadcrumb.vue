<template>
	<div v-if="isShowBreadcrumb" class="layout-navbars-breadcrumb">
		<SvgIcon
			class="layout-navbars-breadcrumb-icon"
			:name="themeConfig.isCollapse ? 'ele-Expand' : 'ele-Fold'"
			:size="20"
			@click="onThemeConfigChange"
		/>
	</div>
</template>

<script lang="ts">
import { reactive, computed, defineComponent } from 'vue';
import { Local } from '@/utils/storage';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '@/stores/themeConfig';

export default defineComponent({
	setup() {
		// 定义变量内容
		const storesThemeConfig = useThemeConfig();
		const { themeConfig } = storeToRefs(storesThemeConfig);
		const state = reactive<BreadcrumbState>({
			breadcrumbList: [],
			routeSplit: [],
			routeSplitFirst: '',
			routeSplitIndex: 1,
		});

		// 动态设置经典、横向布局不显示
		const isShowBreadcrumb = computed(() => {
			const { layout, isBreadcrumb } = themeConfig.value;
			if (layout === 'classic' || layout === 'transverse') return false;
			else return isBreadcrumb ? true : false;
		});
		// 展开/收起左侧菜单点击
		const onThemeConfigChange = () => {
			themeConfig.value.isCollapse = !themeConfig.value.isCollapse;
			setLocalThemeConfig();
		};
		// 存储布局配置
		const setLocalThemeConfig = () => {
			Local.remove('themeConfig');
			Local.set('themeConfig', themeConfig.value);
		};
		return { state, themeConfig, isShowBreadcrumb, onThemeConfigChange };
	}
});

</script>

<style scoped lang="scss">
.layout-navbars-breadcrumb {
	flex: 1;
	height: inherit;
	display: flex;
	align-items: center;
	.layout-navbars-breadcrumb-icon {
		cursor: pointer;
		font-size: 18px;
		color: var(--next-bg-topBarColor);
		height: 100%;
		width: 40px;
		opacity: 0.8;
		&:hover {
			opacity: 1;
		}
	}
	.layout-navbars-breadcrumb-span {
		display: flex;
		opacity: 0.7;
		color: var(--next-bg-topBarColor);
	}
	.layout-navbars-breadcrumb-iconfont {
		font-size: 14px;
		margin-right: 5px;
	}
	:deep(.el-breadcrumb__separator) {
		opacity: 0.7;
		color: var(--next-bg-topBarColor);
	}
	:deep(.el-breadcrumb__inner a, .el-breadcrumb__inner.is-link) {
		font-weight: unset !important;
		color: var(--next-bg-topBarColor);
		&:hover {
			color: var(--el-color-primary) !important;
		}
	}
}
</style>
