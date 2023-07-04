<template>
	<el-container class="layout-container">
		<Aside />
		<el-container class="flex-center" :class="{ 'layout-backtop': !isFixedHeader }">
			<LayoutHeader v-if="showHeader" />
			<Main />
		</el-container>
		<!--<el-backtop target=".layout-backtop .el-scrollbar__wrap"></el-backtop>-->
	</el-container>
</template>

<script lang="ts">
import { onBeforeMount, onUnmounted, getCurrentInstance, defineComponent, computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '@/stores/themeConfig';
import { Local } from '@/utils/storage';
import { useRoute } from 'vue-router';
import Aside from '@/layout/component/aside.vue';
import Main from '@/layout/component/main.vue';
import LayoutHeader from '@/layout/component/header.vue';

export default defineComponent({
	name: 'layout',
	components: { Aside, Main, LayoutHeader },
	setup() {
		const { proxy } = <any>getCurrentInstance();
		const storesThemeConfig = useThemeConfig();
		const { themeConfig } = storeToRefs(storesThemeConfig);
		const showHeader = ref(true);
		// 窗口大小改变时(适配移动端)
		const onLayoutResize = () => {
			if (!Local.get('oldLayout')) Local.set('oldLayout', themeConfig.value.layout);
			const clientWidth = document.body.clientWidth;
			if (clientWidth < 1000) {
				themeConfig.value.isCollapse = false;
				proxy.mittBus.emit('layoutMobileResize', {
					layout: 'defaults',
					clientWidth,
				});
				showHeader.value = true;
			} else {
				proxy.mittBus.emit('layoutMobileResize', {
					layout: Local.get('oldLayout') ? Local.get('oldLayout') : themeConfig.value.layout,
					clientWidth,
				});
				showHeader.value = false;
			}
			document.documentElement.style.setProperty('--app-height', `${window.innerHeight}px`);
		};
		const isFixedHeader = computed(() => {
			return themeConfig.value.isFixedHeader;
		});
		const route = useRoute();
		// 页面加载前
		onBeforeMount(() => {
			onLayoutResize();
			window.addEventListener('resize', onLayoutResize);
		});
		// 页面卸载时
		onUnmounted(() => {
			window.removeEventListener('resize', onLayoutResize);
		});
		return {
			isFixedHeader,
			showHeader,
		};
	},
});
</script>
