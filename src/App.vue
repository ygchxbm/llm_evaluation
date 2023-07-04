<template>
	<el-config-provider :size="getGlobalComponentSize" :locale="i18nLocale">
		<router-view />
	</el-config-provider>
</template>

<script lang="ts">
import { computed, ref, getCurrentInstance, onBeforeMount, onMounted, onUnmounted, nextTick, defineComponent, watch, reactive, toRefs } from 'vue';
import { useRoute } from 'vue-router';
import other from '@/utils/other';

export default defineComponent({
	name: 'app',
	setup() {
		const { proxy } = <any>getCurrentInstance();
		const setingsRef = ref();
		const route = useRoute();
		const state = reactive({
			i18nLocale: null,
		});
		// 获取全局组件大小
		const getGlobalComponentSize = computed(() => {
			return other.globalComponentSize();
		});
		// 设置初始化，防止刷新时恢复默认
		onBeforeMount(() => {
		});
		// 页面加载时
		onMounted(() => {
			nextTick(() => {
				// 设置 i18n，App.vue 中的 el-config-provider
				proxy.mittBus.on('getI18nConfig', (locale: string) => {
					(state.i18nLocale as string | null) = locale;
				});
			});
		});
		// 页面销毁时，关闭监听布局配置/i18n监听
		onUnmounted(() => {
			proxy.mittBus.off('getI18nConfig', () => {});
		});
		// 监听路由的变化，设置网站标题
		watch(() => route.path, () => other.useTitle(), { deep: true });
		return {
			setingsRef,
			getGlobalComponentSize,
			...toRefs(state),
		};
	},
});
</script>

<style>
/* https://at.alicdn.com/t/font_2298093_y6u00apwst.css */
@import url('./theme/iconfont.css');
/* https://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css */
@import url('./theme/font-awesome.css');
</style>