import jwtDecode from 'jwt-decode';

export default {
  data() {
    return {
      user: null,
    };
  },
  created() {
    this.getUser();
  },
  methods: {
    getUser() {
      const token = localStorage.getItem('authToken');
      if (token) {
        this.user = jwtDecode(token);
      }
    },
  },
};
