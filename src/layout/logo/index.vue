<template>
	<div class="layout-logo">
		<a href="/"><img :src="Logo" class="logo" /></a>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserInfo } from '@/stores/userInfo';
import { storeToRefs } from 'pinia';
import Logo from '@/assets/logo.png';

export default defineComponent({
	name: 'layoutLogo',
	emits: ['create'],
	setup() {
		const stores = useUserInfo();
		const { userInfos } = storeToRefs(stores);
		const { name } = userInfos.value;
		return {
			name,
			Logo,
		};
	},
});
</script>

<style scoped lang="scss">
.layout-logo {
	text-align: center;
	padding: 32px 0 45px;
	.logo {
		width: 200px;
	}
}
</style>
