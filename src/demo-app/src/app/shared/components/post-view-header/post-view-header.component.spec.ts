import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostViewHeaderComponent } from './post-view-header.component';

describe('PostViewHeaderComponent', () => {
  let component: PostViewHeaderComponent;
  let fixture: ComponentFixture<PostViewHeaderComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PostViewHeaderComponent]
    });
    fixture = TestBed.createComponent(PostViewHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
