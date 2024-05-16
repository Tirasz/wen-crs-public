import { Component, Input, OnInit } from '@angular/core';
import { GlobalStateService } from '../../../core/services/global-state.service';
import { MatButtonToggleChange } from '@angular/material/button-toggle';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { first } from 'rxjs';

@Component({
  selector: 'app-post-view-header',
  templateUrl: './post-view-header.component.html',
  styleUrls: ['./post-view-header.component.scss']
})
export class PostViewHeaderComponent implements OnInit {

  @Input() isLoading = false;

  sliderValueChange(value: number) {
    this.stateService.setUserQueryParam({
      factor: value
    });
  }

  buttonToggleValueChange(change: MatButtonToggleChange) {
    this.stateService.setUserQueryParam({
      type: change.value
    })
  }

  toggleChannelFilter(value: MatSlideToggleChange) {
    this.stateService.setUserQueryParam({
      filterChannel: value.checked
    })
  }

  factorInitialValue: number;
  typeInitialValue: string;
  toggleInitialValue: boolean;

  ngOnInit(): void {
    this.stateService.getUserQueryParams().pipe(
      first()
    ).subscribe((params) => {
      this.factorInitialValue = params.factor;
      this.typeInitialValue = params.type;
      this.toggleInitialValue = params.filterChannel;
    })
  }

  constructor(private stateService: GlobalStateService) { }

}
