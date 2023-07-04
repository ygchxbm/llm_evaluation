<template>
	<template v-for="val in chils">
		<el-sub-menu :index="val.path" :key="val.path" v-if="val.children && val.children.length > 0">
			<template #title>
				<el-menu-item :index="val.path" style="padding: 0;background: transparent;border: none;">{{ $t(val.meta.title) }}</el-menu-item>
			</template>
			<sub-item :chil="val.children" />
		</el-sub-menu>
		<template v-else>
			<el-menu-item :index="val.path" :key="val.path">
				<template v-if="!val.meta.isLink || (val.meta.isLink && val.meta.isIframe)">{{ $t(val.meta.title) }}</template>
				<template v-else>
					<a :href="val.meta.isLink" target="_blank" rel="opener" class="w100">
						{{ $t(val.meta.title) }}
					</a>
				</template>
			</el-menu-item>
		</template>
	</template>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';

export default defineComponent({
	name: 'navMenuSubItem',
	props: {
		chil: {
			type: Array,
			default: () => [],
		},
	},
	setup(props) {
		// 获取父级菜单数据
		const chils = computed(() => {
			return <any>props.chil;
		});
		return {
			chils,
		};
	},
});
</script>
