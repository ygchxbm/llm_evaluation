import { nextTick } from 'vue';
import '@/theme/loading.scss';

/**
 * 页面全局 Loading
 * @method start 创建 loading
 * @method done 移除 loading
 */
export const NextLoading = {
	// 创建 loading
	start: () => {
		const bodys: Element = document.body;
		const div = <HTMLElement>document.createElement('div');
		div.setAttribute('class', 'loading-next');
		const htmls = `
			<div class="loading-next-box">
				<div class="loading-next-box-warp">
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
					<div class="loading-next-box-item"></div>
				</div>
			</div>
		`;
		div.innerHTML = htmls;
		bodys.insertBefore(div, bodys.childNodes[0]);
		window.nextLoading = true;
	},
	// 移除 loading
	done: () => {
		nextTick(() => {
			window.nextLoading = false;
			const el = <HTMLElement>document.querySelector('.loading-next');
			el?.parentNode?.removeChild(el);
		});
	},
};

export function chartLoading() {
	return {
		graphic: {
			elements: [{
				type: 'group',
				left: 'center',
				top: 'center',
				children: new Array(7).fill(0).map((val, i) => ({
					type: 'rect',
					x: i * 20,
					shape: {
						x: 0,
						y: -40,
						width: 10,
						height: 80
					},
					style: {
						fill: '#5470c6'
					},
					keyframeAnimation: {
						duration: 1000,
						delay: i * 200,
						loop: true,
						keyframes: [
							{
								percent: 0.5,
								scaleY: 0.3,
								easing: 'cubicIn'
							},
							{
								percent: 1,
								scaleY: 1,
								easing: 'cubicOut'
							}
						]
					}
				}))
			}]
		}
	};
}
