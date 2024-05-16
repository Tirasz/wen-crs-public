import { AfterViewInit, Component, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { DummyClientService } from '../../core/services/dummy-client.service';
import { BehaviorSubject, Observable, ReplaySubject, catchError, combineLatest, distinctUntilChanged, filter, first, map, of, switchMap, tap, withLatestFrom } from 'rxjs';
import { Channel, Post } from '../../core/services/types';
import { Router } from '@angular/router';
import { GlobalStateService } from '../../core/services/global-state.service';
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';

@Component({
  selector: 'app-channel-view',
  templateUrl: './channel-view.component.html',
  styleUrls: ['./channel-view.component.scss']
})
export class ChannelViewComponent implements OnInit {

  currentChannel = this.stateService.getCurrentChannel();
  latestTimestamp = new BehaviorSubject<string>("1970-01-01T00:00:00.000Z");
  fetchMore = new BehaviorSubject(false);
  currentPosts = new BehaviorSubject<Post[]>([]);
  isLoading = new BehaviorSubject(false);

  postsToDisplay = this.currentPosts.pipe(
    map(posts => posts.filter(post => Boolean(post.content) && post.content.length >= 10))
  )

  ngOnInit(): void {
    combineLatest([
      this.currentChannel.pipe(
        filter(channel => Boolean(channel)),
        distinctUntilChanged((prev, curr) => prev?.id === curr?.id),
        tap(() => {
          this.currentPosts.next([]);
          this.latestTimestamp.next("1970-01-01T00:00:00.000Z");
          this.fetchMore.next(false);
        })
      ),
      this.latestTimestamp
    ]).pipe(
      switchMap(([channel, timestamp]) => this.dummyClient.getPosts(channel!.id, timestamp)),
      tap(response => this.fetchMore.next(response.more)),
      tap(() => this.isLoading.next(false)),
      map(response => response.posts)
    ).subscribe(posts => {
      let _posts = [...this.currentPosts.value];
      _posts.push(...posts);
      this.currentPosts.next(_posts);
    });

    this.currentChannel.pipe(first()).subscribe(channel => {
      if (!Boolean(channel)) {
        this.router.navigateByUrl('/');
      }
    });
  }

  navigateToPost(post: Post) {
    this.stateService.setCurrentPost(post);
    this.stateService.setCurrentChannel({
      id: post.channelId,
      name: post.channelName
    })
    this.router.navigateByUrl('/post-view' + '?postId=' + encodeURIComponent(post.id));
  }

  fetchNextPage() {
    this.isLoading.next(true);
    this.currentPosts.pipe(
      first(),
      map(posts => posts.sort((a, b) => a.timestamp.localeCompare(b.timestamp))),
      map(sorted => sorted[sorted.length - 1].timestamp)
    ).subscribe(timestamp => {
      this.latestTimestamp.next(timestamp);
    })
  }

  constructor(
    private dummyClient: DummyClientService,
    private stateService: GlobalStateService,
    private router: Router
  ) { }


}
