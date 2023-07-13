<template>
    <div>
      <h1>题库列表</h1>
      <ul>
        <li v-for="dataset in datasets" :key="dataset.id">
          <{{ dataset.name }}
          <button @click="selectDataset(dataset)">选择</button>>
        </li>
      </ul>
  
      <div v-if="selectedDataset">
        <h2>选择语言模型</h2>
        <select v-model="selectedModel">
          <option v-for="model in models" :value="model">{{ model.name }}</option>
        </select>
  
        <button @click="startEvaluation">开始评测</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        datasets: [], // 存储题库列表的数组
        selectedDataset: null, // 选择的题库
        isQuestionnireOpen:false,
        selectedModel: null, // 选择的语言模型
        models: [ // 语言模型列表
          { name: '模型1', id: 1 },
          { name: '模型2', id: 2 },
        ]
      };
    },
    mounted() {
      // 在组件挂载时从后端获取题库列表
      this.fetchDatasets();
    },
    methods: {
      fetchDatasets() {
        // 使用适当的方法从后端获取题库列表
        // 并将其存储到this.datasets中
      },
      selectDataset(dataset) {
        this.selectedDataset = dataset;
      },
      startEvaluation() {
        if (this.selectedDataset && this.selectedModel) {
          // 导航到评测页面，并传递选择的题库和语言模型
          this.$router.push({
            name: 'Evaluation',
            params: {
              datasetId: this.selectedDataset.id,
              modelId: this.selectedModel.id
            }
          });
        } else {
          // 提示用户选择题库和语言模型
          // 或者显示错误信息
        }
      }
    }
  };
  </script>
  