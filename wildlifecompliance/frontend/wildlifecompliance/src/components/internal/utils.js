import Vue from 'vue'
import api from './api'
import {helpers} from '@/utils/hooks' 

export default {
    fetchApplication: function(id){
        return new Promise ((resolve,reject) => {
            Vue.http.get(helpers.add_endpoint_json(api.applications,id)).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });
    },
    fetchOrganisations: function(id){
        return new Promise ((resolve,reject) => {
            Vue.http.get(api.organisations).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });
    },
    fetchOrganisation: function(id){
        return new Promise ((resolve,reject) => {
            Vue.http.get(helpers.add_endpoint_json(api.organisations,id)).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });
    },
    fetchProfile: function(id){
        return new Promise ((resolve,reject) => {
            Vue.http.get(helpers.add_endpoint_json(api.profiles,id)).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });
    },
    fetchUsers: function(id){
        return new Promise ((resolve,reject) => {
            Vue.http.get(api.users).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });
    },
    fetchUser: function(id){
        return new Promise ((resolve,reject) => {
            Vue.http.get(helpers.add_endpoint_json(api.users,id)).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });
    },
    fetchCurrentUser: function (){
        return new Promise ((resolve,reject) => {
            Vue.http.get(api.profile).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });
    },
    fetchCountries: function (){
        return new Promise ((resolve,reject) => {
            Vue.http.get(api.countries).then((response) => {
                resolve(response.body);
            },
            (error) => {
                reject(error);
            });
        });

    },
}
