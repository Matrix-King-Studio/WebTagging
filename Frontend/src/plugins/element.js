import Vue from 'vue'
import {
    Button, Container, Switch,
    Header, Aside, Main, Row, Col,
    Breadcrumb, BreadcrumbItem,
    Tabs, TabPane,
    Menu, Submenu, MenuItem, MenuItemGroup,
    Upload, Tag, Input, Slider, Select, Option, OptionGroup,
    Tooltip,Pagination,Transfer,
    Message,MessageBox,
} from 'element-ui'

Vue.use(Button)
Vue.use(Container)
Vue.use(Switch)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Row)
Vue.use(Col)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(TabPane)
Vue.use(Tabs)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(MenuItemGroup)
Vue.use(Upload)
Vue.use(Tag)
Vue.use(Input)
Vue.use(Slider)
Vue.use(Select)
Vue.use(Option)
Vue.use(OptionGroup)
Vue.use(Tooltip)
Vue.use(Pagination)
Vue.use(Transfer)

Vue.prototype.$message = Message
Vue.prototype.$msgbox = MessageBox
Vue.prototype.$alert = MessageBox.alert
Vue.prototype.$confirm = MessageBox.confirm
Vue.prototype.$prompt = MessageBox.prompt


