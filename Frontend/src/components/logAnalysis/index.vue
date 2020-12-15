<template>
  <div>
    <el-button @click="resetDateFilter">清除日期过滤器</el-button>
    <el-button @click="clearFilter">清除所有过滤器</el-button>
    <el-table
      ref="filterTable"
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="time"
        label="时间"
        sortable
        width="250"
        column-key="time"
        :filters="[
        {text: '2016-05-01', value: '2016-05-01'},
        {text: '2016-05-02', value: '2016-05-02'},
        {text: '2016-05-03', value: '2016-05-03'},
        {text: '2016-05-04', value: '2016-05-04'}]"
        :filter-method="filterHandler">
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        width="100">
      </el-table-column>
      <el-table-column
        prop="task"
        label="任务"
        width="180">
      </el-table-column>
      <el-table-column
        prop="behavior"
        label="行为"
        :formatter="formatter">
      </el-table-column>
      <el-table-column
        prop="identity"
        label="身份"
        width="100"
        :filters="[{ text: '家', value: '家' },
      { text: '公司', value: '公司' }]"
        :filter-method="filterTag"
        filter-placement="bottom-end">
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.identity === '标注员' ? 'primary' : 'success'"
            disable-transitions>{{ scope.row.identity }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
    <div>
      <div id="chartMountNode"></div>
    </div>
  </div>
</template>

<script>
import G2 from "@antv/g2"

export default {
  name: "index",
  data() {
    return {
      chart: null,
      tableData: [
        {
        time: '2020-11-19T14:19:20.153Z',
        name: 'Alex',
        task: "街道数据集",
        behavior: '加载job',
        identity: '标注员'
      }, {
        time: '2020-11-20T14:19:20.153Z',
        name: '007',
        task: "街道数据集",
        behavior: '导出标注数据',
        identity: '管理员'
      }, {
        time: '2020-12-19T14:19:20.153Z',
        name: 'Alex',
        task: "街道数据集",
        behavior: '绘制标注框',
        identity: '标注员'
      }, {
        time: '2020-11-19T14:19:35.153Z',
        name: '007',
        task: "街道数据集",
        behavior: '通过标注数据',
        identity: '质检员'
      }]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.init();
    });
  },
  methods: {
    init() {
      const graphMountNode = document.getElementById("chartMountNode")
      this.chart = new G2.Chart({
        container: graphMountNode,
        width: 1000,
        height: 400
      });

      const data = [{
        company: 'Apple',
        type: '整体',
        value: 30
      }, {
        company: 'Facebook',
        type: '整体',
        value: 35
      }, {
        company: 'Google',
        type: '整体',
        value: 28
      }, {
        company: 'Apple',
        type: '非技术岗',
        value: 40
      }, {
        company: 'Facebook',
        type: '非技术岗',
        value: 65
      }, {
        company: 'Google',
        type: '非技术岗',
        value: 47
      }, {
        company: 'Apple',
        type: '技术岗',
        value: 23
      }, {
        company: 'Facebook',
        type: '技术岗',
        value: 18
      }, {
        company: 'Google',
        type: '技术岗',
        value: 20
      }, {
        company: 'Apple',
        type: '技术岗',
        value: 35
      }, {
        company: 'Facebook',
        type: '技术岗',
        value: 30
      }, {
        company: 'Google',
        type: '技术岗',
        value: 25
      }];
      this.chart.source(data);
      this.chart.scale('value', {
        alias: '占比（%）',
        max: 75,
        min: 0,
        tickCount: 4
      });
      this.chart.axis('type', {
        label: {
          textStyle: {
            fill: '#aaaaaa'
          }
        },
        tickLine: {
          alignWithLabel: false,
          length: 0
        }
      });

      this.chart.axis('value', {
        label: {
          textStyle: {
            fill: '#aaaaaa'
          }
        },
        title: {
          offset: 50
        }
      });
      this.chart.legend({
        position: 'top-center'
      });
      this.chart.interval().position('type*value').color('company').opacity(1).adjust([{
        type: 'dodge',
        marginRatio: 1 / 32
      }]);
      this.chart.render();
    },
    resetDateFilter() {
      this.$refs.filterTable.clearFilter('time');
    },
    clearFilter() {
      this.$refs.filterTable.clearFilter();
    },
    formatter(row, column) {
      return row.behavior;
    },
    filterTag(value, row) {
      return row.tag === value;
    },
    filterHandler(value, row, column) {
      const property = column['property'];
      return row[property] === value;
    }
  }
}
</script>

<style scoped>

</style>