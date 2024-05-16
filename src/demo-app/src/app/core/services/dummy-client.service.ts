import { HttpClient } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Observable, map, of, shareReplay, tap } from 'rxjs';
import { Channel, DummyClientChannelsResponse, DummyClientPostsResponse, Post } from './types';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DummyClientService {
  CLIENT = environment.DUMMY_CLIENT;

  getChannels(nextUrl: string = '/channels') {
    const url = this.CLIENT + nextUrl
    return this.http.get<DummyClientChannelsResponse>(url)
  }

  getPosts(channelId: string, timestamp: string) {
    const url = this.CLIENT + '/channel-posts?channel_id=' + channelId + '&direction=Down&timestamp=' + timestamp;
    return this.http.get<DummyClientPostsResponse>(url);
  }
  constructor(private http: HttpClient) { }

}
