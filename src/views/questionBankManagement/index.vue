<script setup lang="ts">
import {ref, onMounted, computed} from "vue";
import {Question, questionSetDetail, questionSetItem, questionSetList, modifyQuestionSet, modelList, importQuestions, exportQuestions, deleteQuestions} from "@/api";
import {Upload} from '@element-plus/icons-vue';

const selectedQuestionBankId = ref<number>(0)
const questionBankList = ref<questionSetItem[]>([]);
const selectedQuestionBank = ref<Question | {} | null>({});

const createQuestionBankDialogVisible = ref<boolean>(false);
const newQuestionBankName = ref<string>("");
const toLoadQuestionBankDialogVisible = ref<boolean>(false);
let modeNameList = ref<object>({});
const toLoadFile = ref<File | object>({name: '请导入题目文件'});


const endQuestionBankId = computed(() => {
  return questionBankList.value[questionBankList.value.length - 1].id;
})
onMounted(init)

async function changeQuestionItem(id: number) {
  // console.info("id:", id)
  selectedQuestionBankId.value = id
  await questionSetDetail(id).then(res => {
    // console.info("res:", res)
    selectedQuestionBank.value = res;
  }).catch(e => {
    console.info("e:", e)
  })
}

function createQuestionBank() {
  modifyQuestionSet(undefined, newQuestionBankName.value).then((res) => {
    if (res.code !== 0) return
    createQuestionBankDialogVisible.value = false;
    init(res.data.id);
  }).catch(e => {
    console.info("e:", e)
  })
}

async function init(newQuestionBankId?: number) {
  await questionSetList(1).then(res => {
    questionBankList.value = res;
  }).catch(e => {
    console.info("e:", e)
  })

  if (questionBankList.value.length === 0) return
  const questionBankId = (newQuestionBankId as number) || endQuestionBankId.value;
  selectedQuestionBankId.value = questionBankId;
  await questionSetDetail(questionBankId).then(res => {
    if (res === null) {
      return
    }
    selectedQuestionBank.value = res;
  }).catch(e => {
    console.info("e:", e)
  })
}

async function openToLoadDialogDialog() {
  await modelList().then(res => {
    res.forEach(item => {
      const {id, name} = item;
      Reflect.set(modeNameList.value, id, name)
    })
    // console.info("modeNameList.value:", modeNameList.value)
  }).catch(e => {
    console.info(e)
  });
  toLoadQuestionBankDialogVisible.value = true;
}

function openFile(e: any) {
  const node = e.target;
  const reader = new FileReader();
  reader.onload = function fileReadCompleted() {
    // console.info("node.files[0]:", node.files[0])
    toLoadFile.value = node.files[0];
  }
  reader.readAsText(node.files[0]);
}

function toLoadQuestionBank() {
  toLoadQuestionBankDialogVisible.value = false;
  // if(!toLoadModelId.value){
  //   alert('请选择题库')
  //   return
  // }
  // console.info("toLoadFile.value:", toLoadFile.value
  if ((toLoadFile.value as File).name === '请导入题目文件') {
    alert('请上传题目文件')
    return
  }
  importQuestions(selectedQuestionBankId.value, (toLoadFile.value as unknown as File)).then(res => {
    // console.info("res:", res)
    if (res.code === 0) {
      questionSetDetail(selectedQuestionBankId.value).then(res => {
        selectedQuestionBank.value = res;
      }).catch(e => {
        console.info("e:", e)
      })
    }
  }).catch(e => {
    console.info("e:", e)
  })
}

function downloadQuestionBank() {
  location.href = exportQuestions(selectedQuestionBankId.value);
}


async function deleteQuestionBank() {
  await deleteQuestions(selectedQuestionBankId.value).catch(e => {
    console.info("e:", e)
  })
  await init()
}

function openToLoadDialog() {
  const file: Element | null | any = document.querySelector(".upload-input");
  (file as any).value = "";
  toLoadFile.value = {name: '请导入题目文件'};
}

function openCreateDialog() {
  newQuestionBankName.value = "";
}

</script>

<template>
  <div class="question-bank-management">
    <div class="content">
      <div class="aside">
        <ul class="question-name-list">
          <li :class="['question-name-base',selectedQuestionBankId!==item.id?'question-name-unSelected':'question-name-selected']" v-for="item in questionBankList" :key="item.id"
              @click="changeQuestionItem(item.id)">
            {{ item.name }}
          </li>
        </ul>
      </div>
      <div class="main">
        <div class="header">
          <div class="question-bank-title">{{ (selectedQuestionBank as Question).name }}</div>
          <div class="operations">
            <div class="to-load">
              <button @click="openToLoadDialogDialog">导入</button>
              <el-dialog
                  v-model="toLoadQuestionBankDialogVisible"
                  title="导入题目"
                  width="30%"
                  align-center
                  @close="openToLoadDialog"
              >
                <div class="file">
                  <div class="upload">
                    <div class="text">{{ (toLoadFile as File).name }}</div>
                    <div class="upload-sets">
                      <input class="upload-input" type="file" @change="openFile" accept=".xls,.xlsx">
                      <el-button class="upload-btn">
                        <el-icon class="el-icon--right">
                          <Upload/>
                        </el-icon>
                        上传文件
                      </el-button>
                    </div>
                  </div>
                </div>
                <template #footer>
                  <el-button type="primary" @click="toLoadQuestionBank">
                    确定
                  </el-button>
                </template>
              </el-dialog>
            </div>
            <button @click="downloadQuestionBank">下载</button>
            <button @click="deleteQuestionBank">删除</button>

          </div>
        </div>
        <ul class="question-list">
          <li class="question" v-for="item in (selectedQuestionBank as Question).questions">
            <div class="question-title">{{ item.question }}</div>
            <span class="question-style">{{ item.dimension || '无' }}</span>
            <div class="question-answer">{{ item.answer }}</div>
          </li>
        </ul>
      </div>
      <div class="btnS">
        <el-button text @click="createQuestionBankDialogVisible = true">
          新建题库
        </el-button>
        <el-dialog
            v-model="createQuestionBankDialogVisible"
            title="新增题库"
            width="30%"
            align-center
            @close="openCreateDialog"
        >
          <div class="inp">
            <label>题库名称</label>
            <el-input v-model="newQuestionBankName" placeholder="请输入题库名"></el-input>
          </div>
          <template #footer>
            <el-button type="primary" @click="createQuestionBank">
              确定
            </el-button>
          </template>
        </el-dialog>
        <!--        <button>导入题库</button>-->
      </div>
    </div>
  </div>
</template>

<!--suppress SpellCheckingInspection -->
<style scoped lang="scss">
::-webkit-scrollbar-track-piece {
  background-color: #dddee0;
}

.question-bank-management {
  width: 100%;
  height: 100%;
  overflow: hidden;

  .content {
    width: calc(100% - 48px);
    height: calc(100% - 20px);
    margin: 20px 28px 0 20px;
    display: flex;

    .aside {
      width: 140px;

      .question-name-list {
        margin-top: 28px;
        padding-bottom: 40px;
        height: 100%;
        overflow-y: scroll;

        .question-name-base {
          width: 140px;
          height: 32px;
          margin-bottom: 6px;
          cursor: pointer;

          color: #000000b3;
          font-size: 14px;
          font-weight: 400;
          text-align: left;
          line-height: 32px;
          padding: 0 12px;

          text-overflow: ellipsis;
          overflow: hidden;
          word-break: break-all;
          white-space: nowrap;
        }

        .question-name-unSelected {
          background: #EDEDEDFF;
        }

        .question-name-selected {
          background: #C6E8EFFF;
        }
      }
    }

    .main {
      width: calc(100% - 14px);
      height: 100%;
      opacity: 1;
      border: 0 solid #979797ff;
      background: #ffffffff;
      box-shadow: 0 10px 14px 0 #0000001a;
      overflow-y: auto;

      .header {
        display: flex;
        justify-content: space-between;
        margin: 16px 16px 0 30px;

        .question-bank-title {
          margin-top: 14px;
          color: #000000e6;
          font-size: 28px;
          font-weight: bold;
          text-align: center;
          line-height: 28px;
          letter-spacing: 0.24px;
        }

        .operations {
          display: flex;

          .to-load {
            :deep(.el-dialog) {
              width: 500px;
              height: 340px;
              border-radius: 16px;
              opacity: 1;
              border: 0 solid #979797;
              background: #ffffff;

              .el-dialog__header {
                //margin-top: 15px;
                margin: 30px auto;
                padding: 0;
                color: #000000E6;
                font-size: 18px;
                font-weight: 400;
                text-align: center;
                line-height: 28px;
                letter-spacing: 0.24px;

                .el-dialog__title {
                  font-size: 20px;
                }

                .el-dialog__headerbtn {
                  top: 0;
                }
              }

              .el-dialog__body {
                padding: 0;


                .sel {
                  margin-top: 60px;
                  display: flex;
                  justify-content: center;
                  align-items: baseline;

                  label {
                    margin-right: 16px;

                    color: #00000080;
                    font-size: 14px;
                    font-weight: 400;
                    text-align: right;
                    line-height: 22px;
                  }

                  .el-input {
                    width: 330px;
                    height: 36px;

                    color: #000000e6;
                    font-size: 14px;
                    font-weight: 400;
                    text-align: left;
                    line-height: 22px;
                  }

                  .el-select .el-input.is-focus .el-input__wrapper {
                    box-shadow: 0 0 0 1px #00a9ceff inset !important;
                  }

                }

                .file {
                  margin-top: 30px;

                  .upload {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 36px;

                    .text {
                      width: 290px;
                      border: 1px solid #9b9da1;
                      border-right: 0;
                      height: 36px;
                      padding-left: 8px;

                      color: #00000080;
                      font-size: 14px;
                      font-weight: 400;
                      text-align: left;
                      line-height: 34px;
                    }

                    .upload-sets {
                      width: 112px;

                      .upload-input {
                        opacity: 0;
                        font-size: 0;
                        width: 112px;
                        height: 36px;
                        position: absolute;
                        z-index: 10;
                        cursor: pointer;
                        background: #000;
                      }

                      .upload-btn {
                        width: 112px;
                        height: 36px;
                        border-radius: 3px;
                        padding: 5px 16px 5px 18px;
                        //color: #000000E6;
                        font-size: 14px;
                        font-weight: 400;
                        text-align: center;

                        border-color: #00A9CEFF;
                        background: #ededed;
                        color: #00A9CEFF;


                        .el-icon {
                          padding: 0;
                          margin: 0 5px 0 0;
                        }
                      }
                    }
                  }
                }

              }

              .el-dialog__footer {
                margin-top: 60px;
                text-align: center;

                .el-button {
                  width: 112px;
                  height: 40px;
                  border-radius: 3px;
                  opacity: 1;
                  background: #00a9ceff;

                  color: #ffffffe6;
                  font-size: 16px;
                  font-weight: 400;
                  text-align: center;
                  line-height: 24px;
                }
              }
            }


          }

          button {
            width: 40px;
            height: 24px;
            border-radius: 3px;
            opacity: 1;
            border: 1px solid #00a9ceff;
            //margin-left: 10px;
            margin-right: 10px;
            cursor: pointer;

            color: #00A9CEFF;
            font-size: 12px;
            font-weight: 400;
            text-align: center;
            line-height: 24px;
          }

          :nth-child(3) {
            border-color: #E34D59FF;
            color: #E34D59FF;
          }
        }
      }

      .question-list {
        --width: 30px;
        width: calc(100% - 2 * var(--width));
        margin: 30px;

        .question {
          min-height: 150px;
          margin-top: 30px;

          .question-title {
            min-height: 26px;
            margin-bottom: 8px;
            opacity: 1;
            color: #000000e6;
            font-size: 16px;
            font-weight: bold;
            text-align: left;
            line-height: 26px;
          }

          .question-style {
            height: 24px;
            border-radius: 3px;
            opacity: 1;
            border: 1px solid #c6e8efff;
            background: #e8f9fdff;
            padding: 2px 11px;

            color: #00a9ceff;
            font-size: 12px;
            font-weight: 400;
            text-align: center;
            line-height: 20px;
          }

          .question-answer {
            margin-top: 8px;
            min-height: 84px;
            opacity: 1;
            color: #000000b3;
            font-size: 16px;
            font-weight: 400;
            text-align: left;
            line-height: 28px;
          }
        }
      }
    }

    .btnS {
      width: 112px;
      margin-left: 20px;


      button {
        width: 100%;
        height: 40px;
        border: 0;
        border-radius: 3px;
        opacity: 1;
        background: #00a9ceff;
        margin-bottom: 10px;
        cursor: pointer;


        color: #ffffffe6;
        font-size: 16px;
        font-weight: 400;
        text-align: center;
        line-height: 40px;
      }

      :deep(.el-dialog) {
        width: 500px;
        height: 340px;
        border-radius: 16px;
        opacity: 1;
        border: 0 solid #979797;
        background: #ffffff;

        .el-dialog__header {
          margin: 30px auto;
          padding: 0;
          color: #000000E6;
          font-size: 18px;
          font-weight: 400;
          text-align: center;
          line-height: 28px;
          letter-spacing: 0.24px;

          .el-dialog__title {
            font-size: 20px;
          }

          .el-dialog__headerbtn {
            top: 0;
          }
        }

        .el-dialog__body {
          padding: 0;

          .inp {
            display: flex;
            justify-content: center;
            align-items: baseline;

            label {
              margin-right: 16px;

              color: #00000080;
              font-size: 14px;
              font-weight: 400;
              text-align: right;
              line-height: 22px;
            }

            .el-input {
              width: 330px;
              height: 36px;

              color: #000000e6;
              font-size: 14px;
              font-weight: 400;
              text-align: left;
              line-height: 22px;
            }

            .el-input__wrapper.is-focus {
              box-shadow: 0 0 0 1px #00a9ceff inset
            }
          }
        }

        .el-dialog__footer {
          margin-top: 96px;
          text-align: center;

          .el-button {
            width: 112px;
            height: 40px;
            border-radius: 3px;
            opacity: 1;
            background: #00a9ceff;

            color: #ffffffe6;
            font-size: 16px;
            font-weight: 400;
            text-align: center;
            line-height: 24px;
          }
        }
      }
    }

  }

  li {
    list-style: none;
  }

}
</style>
