import { Component, OnInit } from '@angular/core';
import { DummyClientService } from '../../services/dummy-client.service';
import { BehaviorSubject, Observable, delay, first, map, of, tap } from 'rxjs';
import { Channel, ElasticChannel } from '../../services/types';
import { Router } from '@angular/router';
import { GlobalStateService } from '../../services/global-state.service';
import { ElasticClientService } from '../../services/elastic-client.service';

@Component({
  selector: 'app-channel-list',
  templateUrl: './channel-list.component.html',
  styleUrls: ['./channel-list.component.scss']
})
export class ChannelListComponent implements OnInit {

  channels = new BehaviorSubject<ElasticChannel[]>([]);
  nextChannel = new BehaviorSubject<ElasticChannel | undefined>(undefined);
  isLoading = new BehaviorSubject<boolean>(false);

  oldChannels: Observable<Channel[]> = this.channels.pipe(
    map(channels => channels.map(channel => {
      return {
        id: channel.channelId,
        name: channel.channelName
      }
    }))
  )

  ngOnInit(): void {

    this.elasticClient.getChannels().pipe(
      tap(() => this.isLoading.next(true)),
      first(),
      delay(400),
    ).subscribe(response => {
      this.channels.next(response.channels);

      if (response.after_key) {
        this.nextChannel.next(response.after_key)
      }

      this.isLoading.next(false);
    });
  }

  navigateToChannel(channel: Channel) {
    this.router.navigateByUrl('/channel-view' + '?channelId=' + encodeURIComponent(channel.id));
    this.stateService.setCurrentChannel(channel);
  }

  fetchNextPage() {
    this.elasticClient.getChannels(this.nextChannel.value).pipe(
      tap(() => this.isLoading.next(true)),
      first(),
      delay(400),
    ).subscribe(response => {
      const next = this.channels.value;
      next.push(...response.channels);
      this.channels.next(next)

      if (response.after_key) {
        this.nextChannel.next(response.after_key)
      } else {
        this.nextChannel.next(undefined);
      }

      this.isLoading.next(false);
    });
  }

  constructor(
    private readonly elasticClient: ElasticClientService,
    private readonly stateService: GlobalStateService,
    private router: Router
  ) { }

}
