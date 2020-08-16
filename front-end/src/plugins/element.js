import Vue from 'vue'
import {
    Button, Container, Switch,
    Header, Aside, Main, Row, Col,
    Breadcrumb, BreadcrumbItem,
    Tabs, TabPane,
    Menu, Submenu, MenuItem, MenuItemGroup,
    Upload, Tag, Input,
    Message,
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

Vue.prototype.$message = Message
