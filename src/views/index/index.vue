<template>
	<div class="main">
		<div class="head">
			<div class="title">{{title}}</div>
			<el-button type="primary" class="create-btn" @click="goProfile(0)"><el-icon style="marign: 0 20px 0 16px;"><Plus /></el-icon>Create a new character</el-button>
		</div>
		<div class="npclist">
			<template v-for="(npcs, k) in npcGroups">
				<div class="npc" :class="{current: k===0}" v-for="npc in npcs" :key="npc.id" @mouseleave="operMore = false" @click="goNpc(npc.id, k)">
					<img :src="npc.poster" class="poster" />
					<div class="name">
						<el-icon v-if="+npc.train_status === 1 || +npc.train_status === 3" title="Train Data Modified, Not Trained Yet."><ChatDotRound /></el-icon> 
						<el-icon v-if="+npc.train_status === 2" title="Training..."><Lock /></el-icon>
						{{npc.name}}
					</div>
					<div v-if="k > 0 && npc.children.length" class="folder-wrap">
						<div class="folder-mask"></div>
						<img :src="FolderIcon" class="folder-icon" />
					</div>
					<div v-else class="oper">
						<div class="oper-bg"></div>
						<template v-if="!operMore">
							<div class="btn" @click="chatNow(npc.id)">Chat</div>
							<div class="btn" @click="trainNow(npc.id)">Training</div>
							<div class="btn" @click="operMore = true">More</div>
						</template>
						<template v-else>
							<div class="btn" @click="goProfile(0, npc.id)">Derive</div>
							<div class="btn" @click="goProfile(npc.id)">Profile</div>
							<div class="btn">History</div>
							<div class="btn danger" @click="handleDeleteNpc(npc.id)">Delete</div>
						</template>
					</div>
				</div>
			</template>
		</div>
		<el-dialog width="800" style="max-width: 100%" class="chat-dialog" v-model="chatVisible" :close-on-click-modal="false">
			<template #header>
				<div class="chat-header">
					<div class="info">
						<img class="avatar" :src="curNpc.avatar || DefaultAvatar" />
						<span class="title">Chat :</span>Character {{ curNpc.parents ? curNpc.parents.join(' / ') : '' }} / {{curNpc.name}}
					</div>
					<div class="info">
						LLM-Model:
						<el-select v-model="chatModel" style="margin-left: 8px;">
							<el-option value="default" label="Default"></el-option>
							<el-option value="gpt" label="ChatGPT"></el-option>
						</el-select>
					</div>
				</div>
			</template>
			<div class="chat-wrap">
				<div v-for="(message, rindex) in messages" :key="rindex" class="mitem" :class="{ 'from-me': message.role === 'user' }">
					<div class="message">
						<div class="content" :class="{ inputing: messageInputing === rindex}">{{message.content}}</div>
						<div class="oper" v-if="message.role !== 'user'">
							<el-icon class="micon mbtn" title="Copy Original Text" @click="copyMessage(rindex)"><DocumentCopy /></el-icon>
							<el-icon class="micon mbtn" :class="{liked: messageLiked(rindex, true)}" :title="messageLiked(rindex, true) ? 'Liked' : 'Like'" @click="hLikeMessage(rindex, true)">
								<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
							</el-icon>
							<el-icon class="micon mbtn" :class="{liked: messageLiked(rindex, false)}" :title="messageLiked(rindex, false) ? 'Disliked' : 'Dislike'" @click="hLikeMessage(rindex, false)">
								<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path></svg>
							</el-icon>
						</div>
					</div>
				</div>
				<div class="sbottom" :ref="setRef('bottomDom')"></div>
			</div>
			<template #footer>
				<div class="chat-footer">
					<textarea
						placeholder="Send a message..."
						:rows="userInput.split('\n').length || 1"
						@keydown="inputMessage" @input="changeMessage"
						class="text-input r-input"
						v-model="userInput"
						:style="{ height: userInpuHeight ? userInpuHeight + 'px' : 'auto'}">
					</textarea>
					<pre class="mfakeinput text-input" :ref="setRef('fakeInput')">{{userInput}}</pre>
					<button v-if="sending === 0" class="btn-send" :disabled="!userInput" @click="addSendMessage">
						<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-1" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
					</button>
					<div v-else class="btn-sending">
						<span v-for="i in sending" :key="i">.</span>
					</div>
				</div>
			</template>
		</el-dialog>
		<el-dialog width="800" style="max-width: 100%" v-model="trainVisible" :close-on-click-modal="false">
			<template #header>
				<div class="train-header">
					<div class="title">Training Place</div>
					Character {{ curNpc.parents ? curNpc.parents.join(' / ') : '' }} / {{curNpc.name}}
				</div>
			</template>
			<div class="train-wrap">
				<el-form label-width="130px">
					<el-upload accept=".xls,.xlsx" v-model:file-list="trainFile" :ref="setRef('trainFile')" class="input-upload" :limit="1" :on-exceed="handleFileExceed" :auto-upload="false" :show-file-list="false">
						<template #trigger>
							<div class="file-select">
								<div class="file-info">{{ trainFile[0] ? trainFile[0].name : 'Please upload the file' }}</div>
								<el-button class="file-btn">Select</el-button>
							</div>
						</template>
					</el-upload>
					<el-form-item label="Train Type">
						<el-radio-group v-model="trainType" class="train-radio">
							<el-radio label="multiple">Fine-Tuning</el-radio>
							<el-radio label="single">Prompt Database</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="Update Mode">
						<el-radio-group v-model="trainMode" class="train-radio">
							<el-radio label="insert">Insert</el-radio>
							<el-radio label="replace">Replace</el-radio>
						</el-radio-group>
					</el-form-item>
					<div class="tip" v-if="trainMode === 'replace'">Warning: You should export the old data when you choose replace mode.</div>
				</el-form>
			</div>
			<template #footer>
				<div class="train-footer">
					<el-button class="train-btn" @click="exportTrain">Export</el-button>
					<el-button type="primary" class="train-btn import-btn" :loading="training" :disabled="!trainFile.length" @click="importTrain">Import</el-button>
				</div>
			</template>
		</el-dialog>
		<el-dialog width="80%" style="max-width: 100%" v-model="profileVisible" :close-on-click-modal="false" :loading="loading">
			<template #header>
				<div class="train-header">
					<div class="title">Character Profile</div>
					Character {{ curNpc.parents ? curNpc.parents.join(' / ') : '' }} / {{curNpc.name}}
				</div>
			</template>
			<el-form :model="curNpc" label-width="130px">
				<el-form-item label="Name">
					<el-input v-model="curNpc.name" />
				</el-form-item>
				<el-form-item label="Derived From">
					<el-cascader v-model="curNpc.parentIds" clearable :disabled="curNpc.id > 0" :options="npcAllGroup" style="width: 100%" :props="{value: 'id', label: 'name', checkStrictly: true}" />
				</el-form-item>
				<el-form-item label="Personality Data">
					<el-input v-model="curNpc.personality_data" type="textarea" />
				</el-form-item>
				<el-form-item label="World Base Knowledge">
					<el-input v-model="curNpc.world_base_knowledge" type="textarea" />
				</el-form-item>
				<el-form-item label="Location Knowledge">
					<el-input v-model="curNpc.location_knowledge" type="textarea" />
				</el-form-item>
				<el-form-item label="Avatar">
					<el-upload class="avatar-uploader" action="/api/common.uploadFile?site=oasisme_npc" :show-file-list="false" :on-success="handleUploadSuccess('avatar')" :on-error="handleUploadError" accept="images/*">
						<img v-if="curNpc.avatar" :src="curNpc.avatar" class="avatar" />
						<el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
					</el-upload>
				</el-form-item>
				<el-form-item label="Poster">
					<el-upload class="avatar-uploader" action="/api/common.uploadFile?site=oasisme_npc" :show-file-list="false" :on-success="handleUploadSuccess('poster')" :on-error="handleUploadError" accept="images/*">
						<img v-if="curNpc.poster" :src="curNpc.poster" class="avatar" />
						<el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
					</el-upload>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="train-footer">
					<el-button type="primary" @click="handleSaveProfile" :loading="profileSaving" class="train-btn">Submit</el-button>
				</div>
			</template>
		</el-dialog>
	</div>
</template>

<script lang="ts">
import { nextTick, watch, reactive, toRefs } from 'vue';
import { ElMessageBox, ElMessage, genFileId } from 'element-plus';
import type { UploadInstance, UploadProps, UploadRawFile, UploadUserFile } from 'element-plus'
import { useRouter } from 'vue-router';
import { Plus, DocumentCopy, ChatDotRound, Lock } from '@element-plus/icons-vue';
import useClipboard from 'vue-clipboard3';
import { setTitle } from '@/utils/other';
import { Npc, npcList, npcDetail, chat, Message, FileTuneDataType, exportFineTune, importFineTune, saveNpc, deleteNpc } from '@/api';
import Npc1 from '@/assets/npc1.jpg';
import Npc2 from '@/assets/npc2.jpg';
import DefaultAvatar from '@/assets/avatar.png';
import FolderIcon from '@/assets/folder.png';

interface NpcTree extends Npc {
	parents: string[];
	parentIds: number[];
	children: NpcTree[];
}

export default {
	name: 'Chat',
	components: { Plus, DocumentCopy, ChatDotRound, Lock },
	setup() {
		const router = useRouter();
		const state = reactive({
			npcGroups: [] as NpcTree[][],
			title: '',
			operMore: false,
			loading: false,
			filterNpc: -1,
			curNpc: { avatar: '', id: 1, name: 'Perfectionist' } as NpcTree,
			chatVisible: false,
			userInput: '',
			userInpuHeight: 0,
			sending: 0,
			messages: [] as Message[],
			chatModel: 'default' as 'defalut' | 'gpt',
			messageInputing: -1,
			trainVisible: false,
			trainType: 'multiple' as FileTuneDataType,
			trainFile: [] as UploadUserFile[],
			training: false,
			trainMode: 'insert' as 'replace' | 'insert',
			profileVisible: false,
			profileSaving: false,
			npcAllGroup: [] as NpcTree[],
		});
		const refDoms = {
			bottomDom: null as HTMLElement | null,
			fakeInput: null as HTMLElement | null,
			trainFile: null as UploadInstance | null,
		};
		const sessionId = `${Date.now()}`;
		let sendingTimer: ReturnType<typeof setInterval>;
		let stopSignal: AbortController;
		const { toClipboard } = useClipboard();
		const npcAll: Record<number, NpcTree> = {};
		const cacheMessages: Record<number, Message[]> = {};
		let cacheSid = '';

		function addDbMessage() {
			// addMessage(nMessage).then(id => {
			// 	nMessage.id = id;
			// 	const index = session.value.messages.findIndex(x => +x.id === +id);
			// 	if(index >= 0) {
			// 		session.value.messages[index] = nMessage;
			// 	} else {
			// 		session.value.messages.push(nMessage)
			// 	}
			// }).catch(e => {
			// 	console.error('addMessage err', e);
			// })
		}

        function sendMessage(index: number) {
			const messageLast = state.messages.length - 1;
			sendingTimer = setInterval(() => {
				state.sending = state.sending > 2 ? 1 : state.sending + 1;
			}, 1000);
			state.messageInputing = index;
			stopSignal = new AbortController();
			const prompt = state.messages[messageLast - 1].content;
			// const msgIndex = Math.floor(messageLast / 2);
			// const startTime = Date.now();
            return chat(state.curNpc.model_id || state.curNpc.id, prompt, `${state.curNpc.id}${sessionId}`, stopSignal).then(res => {
                state.messages[index].content = res.text ? res.text.text : 'Api Error';
				cacheMessages[state.curNpc.id] = state.messages;
				if(index === messageLast) {
					nextTick(scrollBottom);
				}
				state.messageInputing = -1;
				// const timecost = Date.now() - startTime;
				// const completion = state.messages[index].content;
				// addDbMessage({ id: 0, session_id: session.value.id, msg_index: msgIndex, prompt, completion, time_cost: timecost, score: 0, chat_id: res.id })
				clearInterval(sendingTimer);
				state.sending = 0;
                return res;
            }).catch(e => {
				if(!(e instanceof DOMException && e.name == "AbortError")) {
					ElMessage.error({ message: e.toString(), duration: 0, showClose: true });
				}
                state.messageInputing = -1;
                console.error('sendMessage err', e);
				clearInterval(sendingTimer);
				state.sending = 0;
            });
		}

		function addSendMessage() {
			if(!state.userInput || state.sending > 0) {
                return;
            }
			const uMessage: Message = { role: "user", content: state.userInput };
            state.messages.push(uMessage);
			nextTick(scrollBottom);
			const index = state.messages.length;
            state.messages.push({ role: 'assistant', content: '' });
            state.userInput = "";
			state.userInpuHeight = 0;
			sendMessage(index);
			state.sending = 2;
		}

		function stopSending() {
			if(stopSignal) {
				stopSignal.abort('cancel');
			}
		}

        function scrollBottom() {
            refDoms.bottomDom && refDoms.bottomDom.scrollIntoView();
        }

		function messageLiked(mindex: number, isLike: boolean) {
			// const item = session.value.messages[Math.floor(mindex/2)];
			// return item && item.score === (isLike ? 1 : -1);
		}

		function hLikeMessage(mindex: number, isLike: boolean) {
			// const item = session.value.messages[Math.floor(mindex/2)];
			// const nScore = (isLike ? 1 : -1);
			// if(item) {
			// 	item.score = +item.score === nScore ? 0 : nScore;
			// 	likeMessage(item.id, item.score);
			// }
		}

		function chatNow(id: number) {
			state.curNpc = npcAll[id];
			state.chatVisible = true;
			state.messages = cacheMessages[id] || [];
		}

		function trainNow(id: number) {
			state.curNpc = npcAll[id];
			state.trainVisible = true;
		}

		const handleFileExceed: UploadProps['onExceed'] = (files) => {
			refDoms.trainFile?.clearFiles()
			const file = files[0] as UploadRawFile
			file.uid = genFileId()
			refDoms.trainFile?.handleStart(file)
		}

		function importTrain() {
			state.training = true;
			importFineTune(state.curNpc.id, state.trainType, state.trainMode, state.trainFile[0].raw as File).then(res => {
				state.training = false;
				ElMessage.success('Import success');
			}).catch(e => {
				state.training = false;
				ElMessageBox.alert(`Import Failed: ${e}`);
				console.error('importFineTune error', e);
			})
		}

		function exportTrain() {
			location.href = exportFineTune(state.curNpc.id, state.trainType);
		}

		function goProfile(id: number, parentId?: number) {
			state.loading = true;
			state.profileVisible = true;
			if(id > 0) {
				npcDetail(id).then(res => {
					if(!res) {
						throw 'Null return';
					}
					state.loading = false;
					state.curNpc = { ...npcAll[id], ...res };
				}).catch(e => {
					state.loading = false;
					console.error('npcDetail err', e);
				})
			} else {
				const parentIds: number[] = parentId ? npcAll[parentId].parentIds.concat(parentId) : [];
				state.curNpc = { id: 0, parent_id: 0, name: 'New', avatar: '', poster: '', personality_data: '', world_base_knowledge: '', location_knowledge: '', parentIds, parents: [], children: [] };
			}
		}

		function handleSaveProfile() {
			const plen = state.curNpc.parentIds.length;
			state.curNpc.parent_id = plen > 0 ? state.curNpc.parentIds[plen-1] : 0;
			state.profileSaving = true;
			saveNpc({ ...state.curNpc, parentIds: undefined, parents: undefined, children: undefined } as Npc).then(() => {
				state.profileSaving = false;
				state.profileVisible = false;
				ElMessage.success('Save Success');
				window.location.reload();
			}).catch(e => {
				state.profileSaving = false;
				ElMessageBox.alert(`${e}`);
				console.error('saveNpc', e);
			})
		}

		function initNpcList(sid: string) {
			state.loading = true;
			state.title = sid === 'all' ? 'Show All' : 'Character Tree';
			cacheSid = sid;
			Object.keys(npcAll).forEach(k=>delete(npcAll[k]));
			npcList().then(res => {
				const tree: NpcTree[] = [];
				res.forEach(x => npcAll[x.id] = { ...x, parents: [], parentIds: [], children: [], poster: x.poster || (Math.random() > 0.5 ? Npc1 : Npc2) });
				res.forEach(x => {
					if(+x.parent_id === 0) {
						tree.push(npcAll[x.id]);
					} else if(npcAll[x.parent_id]) {
						npcAll[x.parent_id].children.push(npcAll[x.id]);
						npcAll[x.id].parents.push(npcAll[x.parent_id].name);
						npcAll[x.id].parentIds.push(x.parent_id);
					} else {
						console.error('not found npc', x.parent_id);
					}
				});
				const recSetParents = function(item: NpcTree, mkey: 'parents' | 'parentIds', curr: (string | number)[]) {
					if(item.parent_id > 0 && npcAll[item.parent_id]) {
						return (npcAll[item.parent_id][mkey] as (string | number)[]).concat(curr);
					}
					return curr;
				};
				Object.values(npcAll).forEach(item => {
					item.parents = recSetParents(item, 'parents', item.parents) as string[];
					item.parentIds = recSetParents(item, 'parentIds', item.parentIds) as number[];
				});
				if(sid === 'all') {
					state.npcGroups = [[], Object.values(npcAll)];
					setTitle(state.title);
				} else if(sid === 'tree') {
					state.npcGroups = [[], tree];
					setTitle(state.title);
				} else {
					state.npcGroups = [[npcAll[sid]], npcAll[sid].children];
					state.title = `${npcAll[sid].parents ? npcAll[sid].parents.join(' / ') : '' } / ${npcAll[sid].name}`;
					setTitle(npcAll[sid].name);
				}
				state.npcAllGroup = tree;
				state.loading = false;
			}).catch(e => {
				state.loading = false;
				console.error('npcList err', e);
				ElMessageBox.alert(`${e}`);
			})
		}

		function goNpc(id: number, groupIndex: number) {
			const npc = npcAll[id];
			if(groupIndex > 0 && npc.children.length > 0) {
				router.push(`/npc/${id}`);
			}
		}

		function handleUploadSuccess(field: 'avatar' | 'poster') {
			return (url: string) => state.curNpc[field] = url
		}

		function handleUploadError(e: Error) {
			ElMessage.error(`${e}`);
		}

		function handleDeleteNpc(id: number) {
			ElMessageBox.confirm('Sure to Delete?').then(() => {
				deleteNpc(id).then(() => {
					ElMessage.success('Delete Success');
					if(state.npcGroups[0][0] && state.npcGroups[0][0].id === id) {
						router.replace('/npc/all');
					} else {
						window.location.reload();
					}
				}).catch(e => {
					ElMessageBox.alert(`${e}`);
					console.error('saveNpc', e);
				})
			}).catch(()=>{});
		}

        watch(() => router.currentRoute.value.params.sid, sid => initNpcList(sid as string), { immediate: true });
        
		return {
			...toRefs(state),
			inputMessage(e: KeyboardEvent) {
				if(!e.shiftKey && e.key === 'Enter') {
					e.preventDefault();
					addSendMessage();
				}
			},
			changeMessage() {
				nextTick(() => state.userInpuHeight = refDoms.fakeInput ? refDoms.fakeInput.scrollHeight : 0);
			},
			addSendMessage,
            sendMessage,
			stopSending,
			reSendMessage() {
				const index = state.messages.length - 1;
				state.messages[index] = { role: 'assistant', content: '' };
				sendMessage(index);
			},
			setRef(key: 'bottomDom' | 'fakeInput') {
				return (el: any) => refDoms[key] = el;
			},
			copyMessage(index: number) {
				toClipboard(state.messages[index].content).then(() => ElMessage.success('Copied'));
			},
			messageLiked,
			hLikeMessage,
			DefaultAvatar,
			chatNow,
			trainNow,
			handleFileExceed,
			exportTrain,
			importTrain,
			goProfile,
			handleSaveProfile,
			FolderIcon,
			goNpc,
			handleUploadSuccess,
			handleUploadError,
			handleDeleteNpc,
		}
	}
}

</script>

<style scoped lang="scss">
	.main {
		padding: 20px 10px;
	}
	.head {
		display: flex;
		justify-content: space-between;
		.title {
			color: #263131ff;
			font-size: 24px;
			font-weight: 600;
			padding-left: 15px;
		}
		.create-btn {
			padding: 8px 24px;
			height: 40px;
			border-radius: 3px;
			background: #36a6bf;
			&:hover {
				color: rgba(255, 255, 255, 0.9);
				background: #2d97af;
			}
		}
	}
	.npclist {
		display: flex;
		flex-wrap: wrap;
		.npc {
			width: 280px;
			height: 420px;
			border-radius: 10px;
			background: #fff;
			color: rgb(38, 49, 49);
			box-shadow: 0 4px 14px 0 rgba(38, 49, 49, 0.1);
			margin: 15px;
			padding: 10px;
			text-align: center;
			cursor: pointer;
			position: relative;
			.poster {
				width: 100%;
				height: 370px;
				border-radius: 8px;
				object-fit: scale-down;
			}
			.name {
				font-size: 16px;
				font-weight: 700;
				padding-top: 4px;
				position: relative;
    			z-index: 2;
			}
			.oper {
				display: none;
				width: 100%;
				height: 100%;
				position: absolute;
				z-index: 1;
				top: 0;
				left: 0;
				flex-direction: column;
				justify-content: center;
				align-items: center;
				.oper-bg {
					background: rgba(0, 0, 0, 0.4);
					height: 370px;
					border-radius: 8px;
					position: absolute;
					width: calc(100% - 20px);
					top: 10px;
				}
				.btn {
					width: 132px;
					height: 40px;
					border-radius: 3px;
					background: #fff;
					text-align: center;
					opacity: 0.9;
					color: #000;
					font-size: 16px;
					font-family: "PingFang SC";
					line-height: 40px;
					margin: 10px 0;
					&:hover {
						background: #d9e4e4;
					}
					&.danger {
						color: #fff;
						background: #e34d59;
						&:hover {
							background: #c9353f;
						}
					}
				}
			}
			&:hover {
				.oper {
					display: flex;
				}
			}
			.folder-wrap {
				position: absolute;
				width: 100%;
				height: 100%;
				z-index: 1;
				top: 0;
				left: 0;
				display: flex;
				justify-content: center;
				align-items: center;
				.folder-icon {
					width: 50px;
					height: 50px;
					opacity: 0.5;
				}
				.folder-mask {
					background: rgba(170, 177, 177, 0.9);
					position: absolute;
					width: 100%;
					height: 370px;
					z-index: -1;
					top: 10px;
					left: 0;
					filter: blur(20px);
				}
			}
			&.current {
				background: #163039;
				color: #ffffffff;
			}
		}
	}
	.chat-wrap {
		min-height: 720px;
		overflow-y: auto;
		margin: 8px 0;
		padding: 10px 25px;
		background: #fff;
		.mitem {
			display: flex;
			margin-bottom: 20px;
			&.from-me {
				justify-content: end;
				.message {
					background: #36a6bf;
 					color: #ffffff;
				}
			}
			.message {
				padding: 11px 12px;
				line-height: 1.5rem;
				position: relative;
				background: #f3f2f4;
				color: rgba(0, 0, 0, 0.9);
				font-size: 14px;
				font-family: "PingFang SC";
				border-radius: 8px;
				.oper {
					position: absolute;
					right: 0;
					top: -18px;
					opacity: 0;
					transition-duration: .5s;
					transition-property: opacity;
					&:hover {
						opacity: 1;
					}
				}
				&:hover {
					.oper {
						opacity: 1;
					}
				}
				.content {
					line-height: 2.0;
					white-space: pre-line;
					word-break: break-word;
					&.inputing::after {
						content: '|';
						animation: 0.6s van-cursor-flicker infinite;
					}
				}
			}
		}
	}
	.chat-footer {
		display: flex;
		justify-content: space-between;
    	align-items: flex-end;
			.text-input {
			background: #f2f2f2;
			border: none;
			font-size: 16px;
			resize: none;
			width: 745px;
			padding: 8px 10px;
			overflow: hidden;
			border-radius: 8px;
			min-height: 34px;
		}
		.r-input {
			overflow-y: auto;
			max-height: calc(var(--app-height) - 100px);
		}
		.mfakeinput {
			position: absolute;
			top: -100vh;
			left: -100vw;
			word-break: break-all;
			white-space: pre-line;
			padding-left: 1rem;
		}
		.btn-send {
			color: #36A6BF;
			padding: 0.25rem;
			font-size: 20px;
			border: none;
			background: transparent;
			cursor: pointer;
			opacity: 0.8;
			display: flex;
			padding-bottom: 6px;
		}
		.btn-send:hover {
			opacity: 1;
		}
		.btn-send:disabled {
			opacity: 0.4;
			color: rgb(142, 142, 160);
			cursor: default;
		}
		.btn-sending {
			font-size: 20px;
			padding-bottom: 6px;
			color: rgba(142,142,160,1);
		}
	}
	.chat-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		.info {
			display: flex;
    		align-items: center;
			font-family: "PingFang SC";
			color: rgba(0, 0, 0, 0.7);
			font-size: 14px;
			.avatar {
				width: 40px;
				height: 40px;
				border-radius: 50%;
				margin-right: 14px;
			}
			.title {
				font-weight: 600;
				text-align: left;
				font-size: 18px;
				margin-right: 8px;
			}
		}
	}
	.train-wrap {
		text-align: center;
		padding-bottom: 120px;
		.input-upload {
			.file-select {
				display: flex;
				margin-bottom: 30px;
			}
			.file-info {
				width: 505px;
				height: 40px;
				color: rgba(0, 0, 0, 0.3);
				font-size: 16px;
				line-height: 40px;
				border-radius: 3px 0 0 3px;
				border: 1px solid #dcdcdc;
				text-align: left;
				padding: 0 12px;
				border-right: none;
			}
			.file-btn {
				height: 40px;
			}
		}
		.train-radio {
			:deep(.el-radio.el-radio--small) {
				width: 90px;
			}
			:deep(.el-radio.el-radio--small .el-radio__label) {
				font-size: 14px;
			}
			:deep(.el-radio.el-radio--small .el-radio__inner) {
				width: 14px;
				height: 14px;
			}
		}
		.tip {
			color: #e34d59;
		}
	}
	.train-header {
		text-align: center;
		color: rgba(0, 0, 0, 0.7);
		font-size: 14px;
		.title {
			font-size: 18px;
			font-weight: 700;
			text-align: center;
			padding: 20px 0 10px;
		}
	}
	.train-footer {
		text-align: center;
		.train-btn {
			font-size: 16px;
			font-weight: 700;
			height: 40px;
			line-height: 40px;
			padding: 0 36px;
		}
	}
	.micon {
		margin-right: 8px;
	}
	.mbtn {
		cursor: pointer;
	}
	.mbtn.liked {
		color: #29d;
	}
	.avatar-uploader {
		.avatar {
			width: 120px;
			height: 120px;
			object-fit: scale-down;
		}
		:deep(.el-upload) {
			border: 1px dashed var(--el-border-color);
			border-radius: 6px;
			cursor: pointer;
			position: relative;
			overflow: hidden;
			transition: var(--el-transition-duration-fast);
		}
		:deep(.el-upload:hover) {
			border-color: var(--el-color-primary);
		}
		.avatar-uploader-icon {
			font-size: 28px;
			color: #8c939d;
			width: 120px;
			height: 120px;
			text-align: center;
		}
	}
	@keyframes van-cursor-flicker {
		from {
			opacity: 0;
		}
		50% {
			opacity: 1;
		}
		100% {
			opacity: 0;
		}
	}
</style>

<style>
	.chat-dialog {
		max-width: 100%;
		background: #f2f2f2;
	}
	.chat-dialog .el-dialog__body {
		padding: 0;
	}
	.chat-dialog .el-dialog__footer {
		padding: 10px;
		background: #fff;
	}
	.chat-dialog .el-dialog__header {
		background: #fff;
		margin-right: 0;
	}
	.chat-dialog .el-dialog__headerbtn {
		top: -10px;
		right: -10px;
	}
</style>