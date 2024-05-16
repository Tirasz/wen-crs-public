import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { GlobalStateService } from '../../core/services/global-state.service';
import { Router } from '@angular/router';
import { BehaviorSubject, ReplaySubject, Subject, combineLatestWith, debounceTime, delay, distinctUntilChanged, distinctUntilKeyChanged, filter, first, forkJoin, map, mergeMap, of, shareReplay, switchMap, takeUntil, tap, withLatestFrom } from 'rxjs';
import { ElasticClientService } from '../../core/services/elastic-client.service';
import { ElasticClientQueryParams, Post, TextQueryTypes } from '../../core/services/types';
import { DummyClientService } from '../../core/services/dummy-client.service';
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';

@Component({
  selector: 'app-post-view',
  templateUrl: './post-view.component.html',
  styleUrls: ['./post-view.component.scss']
})
export class PostViewComponent implements OnInit, OnDestroy {
  @ViewChild(CdkVirtualScrollViewport) virtualScroll: CdkVirtualScrollViewport;

  private onDestroy$ = new Subject<void>();

  currentPost = this.stateService.getCurrentPost().pipe(
    filter(post => Boolean(post)),
    distinctUntilChanged(),
    shareReplay(1)
  );

  currentChannel = this.stateService.getCurrentChannel().pipe(
    filter(channel => Boolean(channel)),
    distinctUntilChanged(),
    shareReplay(1)
  );

  currentUserParams = this.stateService.getUserQueryParams().pipe(
    distinctUntilChanged(),
    shareReplay(1)
  )

  pageFrom = new BehaviorSubject(0);
  recommendations = new BehaviorSubject<Post[]>([]);
  isLoading = new BehaviorSubject(false);

  navigateToPost(post: Post) {
    this.stateService.setCurrentPost(post);
    this.stateService.setCurrentChannel({
      id: post.channelId,
      name: post.channelName
    })
    this.ngOnDestroy();
    this.router.navigateByUrl('/post-view' + '?postId=' + encodeURIComponent(post.id));
    this.virtualScroll.scrollToIndex(0);
    this.ngOnInit();
  }

  fetchNextPage() {
    this.pageFrom.pipe(first()).subscribe(value => {
      this.pageFrom.next(value + 10)
    });
  }

  ngOnInit(): void {
    // Navigate away on weird state
    this.stateService.getCurrentPost().pipe(
      filter(post => !Boolean(post)),
      first(),
    ).subscribe(() => {
      this.router.navigateByUrl('/')
    });

    // Reset recommendations when user query params change
    this.currentUserParams.pipe(
      distinctUntilChanged(),
      takeUntil(this.onDestroy$)
    ).subscribe(() => {
      this.recommendations.next([]);
      this.pageFrom.next(0);
    });

    // Add recommendations to array when 'from' emits
    this.pageFrom.pipe(
      tap(() => this.isLoading.next(true)),
      debounceTime(700),
      withLatestFrom(this.currentUserParams, this.currentPost, this.currentChannel),
      switchMap(([from, params, post, channel]) => {
        let queryParams: ElasticClientQueryParams = {
          from,
          factor: params.factor
        };
        if (params.filterChannel) {
          queryParams['channelId'] = channel!.id;
        }
        return this.elasticService.getRecommendations(post!.id, params.type, queryParams)
      }),
      takeUntil(this.onDestroy$)
    ).subscribe((posts) => {
      this.isLoading.next(false);
      let currentArray = this.recommendations.value;
      currentArray.push(...posts);
      this.recommendations.next(currentArray);
    });

    // Reset query params on init
    this.pageFrom.next(0);
  }

  ngOnDestroy(): void {
    this.onDestroy$.next();
    this.onDestroy$.complete();
  }

  constructor(
    private stateService: GlobalStateService,
    private elasticService: ElasticClientService,
    private dummyClientService: DummyClientService,
    private router: Router
  ) { }


}
