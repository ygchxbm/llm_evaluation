
<template>
	<div v-if="isShowBreadcrumb" class="layout-navbars-breadcrumb">
	  <el-breadcrumb separator-class="el-icon-arrow-right">
		<el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
		<el-breadcrumb-item :to="{path:'/transit'}">发起评测</el-breadcrumb-item>
	  </el-breadcrumb>
	</div>
  </template>
  
  <script>
  import { reactive,computed, defineComponent } from 'vue';
  import { useRoute } from 'vue-router';
	import { Local } from '@/utils/storage';
	import { storeToRefs } from 'pinia';
	import { useThemeConfig } from '@/stores/themeConfig';
  export default defineComponent({
	setup() {
	  	const route = useRoute();
	  	const storesThemeConfig = useThemeConfig();
		const { themeConfig } = storeToRefs(storesThemeConfig);
	  // 获取面包屑导航标签
	  const crumbLabel = computed(() => {
		const paths = route.path.split('/');
		paths.shift();
		return paths.map((pathSegment, index) => {
		  return getLabel(pathSegment);
		}).join(' > ');
	  });
  
	  // 获取标签
	  const getLabel = (pathSegment) => {
		// 根据路径段获取标签
		// ...
	  };
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
  
	  return { crumbLabel, isShowBreadcrumb, themeConfig, isShowBreadcrumb, onThemeConfigChange };
	}
  });
  </script>
  
  <style scoped>
  .layout-navbars-breadcrumb {
	margin-left: 50px;
	flex: 1;
	height: inherit;
	display: flex;
	margin-top: 20px;
	width: 112px;
	height: 40px;
	align-items: center;
	color: #00000066;
	font-size: 14px;
	font-weight: 400;
	font-family: "PingFang SC";
	text-align: left;
	line-height: 22px;
  }
  </style>