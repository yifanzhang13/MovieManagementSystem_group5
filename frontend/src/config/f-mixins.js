import {mapActions, mapState} from 'vuex'
import * as FDEX from '@/f-dex'
import dayjs from 'dayjs'

export const oscarMixin = {
  data() {
    return {
      dayjs
    }
  },
  created() {
    this.initUserAction()
  },
  computed: {
    ...mapState(['userInfoState']), // this.$store.state.userInfoState
  },
  components: FDEX,
  methods: {
    ...mapActions(['initUserAction']),
  },
}
