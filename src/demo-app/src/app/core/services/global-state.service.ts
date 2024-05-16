import { Injectable } from '@angular/core';
import { BehaviorSubject, map } from 'rxjs';
import { Channel, ElasticClientQueryParams, Post, State, TextQueryTypes, UserQueryParam } from './types';

const defaultState: State = {
  userQueryParams: {
    factor: 0.7,
    filterChannel: false,
    type: TextQueryTypes.MML
  }
};

@Injectable({
  providedIn: 'root'
})
export class GlobalStateService {

  currentState = new BehaviorSubject<State>({ ...defaultState });

  setCurrentChannel(channel: Channel) {
    this.currentState.next({ ...this.currentState.value, currentChannel: channel })
  }

  getCurrentChannel() {
    return this.currentState.pipe(
      map(state => state.currentChannel)
    )
  }

  setCurrentPost(post: Post) {
    this.currentState.next({ ...this.currentState.value, currentPost: post })
  }

  getCurrentPost() {
    return this.currentState.pipe(
      map(state => state.currentPost)
    )
  }

  setUserQueryParam(value: Partial<UserQueryParam>) {
    const currentState = this.currentState.value;
    this.currentState.next({ ...currentState, userQueryParams: { ...currentState.userQueryParams, ...value } });
  }

  getUserQueryParams() {
    return this.currentState.pipe(
      map(state => state.userQueryParams)
    )
  }

  resetUserQueryParams() {
    const currentState = this.currentState.value;
    this.currentState.next({ ...currentState, userQueryParams: defaultState.userQueryParams });
  }

  constructor() {
    //this.currentState.subscribe(state => console.log(state))
  }
}
