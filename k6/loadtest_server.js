import http from 'k6/http';
export let options = {
  discardResponseBodies: true,
  scenarios: {
    contacts: {
      executor: 'externally-controlled',
      duration: 0
    },
  },
};

export default function () {
  http.get(`http://${__ENV.ENDPOINT}/`);
}
