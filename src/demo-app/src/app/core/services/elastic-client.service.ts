import { Injectable } from '@angular/core';
import { ElasticChannelInfoParams, ElasticChannelInfoResponse, ElasticClientQueryParams, ElasticClientQueryResponse, Post, TextQueryTypes } from './types';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map, tap } from 'rxjs';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ElasticClientService {
  CLIENT = environment.ELASTIC_CLIENT;


  getChannels(params?: ElasticChannelInfoParams): Observable<ElasticChannelInfoResponse> {
    const url = this.CLIENT + '/channel-info';
    const httpParams = new HttpParams({ fromObject: params });
    console.log(httpParams)
    return this.http.get<ElasticChannelInfoResponse>(url, { params: httpParams });
  }

  toPost(response: ElasticClientQueryResponse): Post {
    return {
      id: response._id,
      author: response._source.author,
      content: (response._source.de || response._source.en || response._source.hu)!,
      embed: response._source.embed,
      channelId: response._source.channelId,
      channelName: response._source.channelName,
      timestamp: response._source.createdDate
    };
  }

  getRecommendations(
    postId: string,
    type: TextQueryTypes = TextQueryTypes.MML,
    params: ElasticClientQueryParams = {},
  ): Observable<Post[]> {
    const encodedId = encodeURIComponent(postId.replace(/\//g, "(xd)"));
    const url = this.CLIENT + '/' + type + '/' + encodedId;
    if (params.channelId) {
      params['channelId'] = encodeURIComponent(params.channelId.replace(/\//g, "(xd)"))
    }
    console.log('GETTING NEW RECOMMENDATIONS WITH PARAMS: ')
    console.log(params, type)
    const httpParams = new HttpParams({ fromObject: params });
    return this.http.get<ElasticClientQueryResponse[]>(url, { params: httpParams }).pipe(
      tap((asd) => console.log(asd)),
      map(responses => responses.map(this.toPost))
    );
  }

  constructor(private http: HttpClient) { }
}
