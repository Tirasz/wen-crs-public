
export type Channel = {
  id: string,
  name: string
}

export type DummyClientChannelsResponse = {
  channels: Channel[],
  next?: string
}

export type DummyClientPostsResponse = {
  posts: Post[],
  more: boolean
}

export type Post = {
  id: string,
  author: string,
  content: string,
  embed?: string,
  channelId: string,
  channelName: string,
  timestamp: string,
  updateTimestamp?: string
}

export type State = {
  currentChannel?: Channel;
  currentPost?: Post;
  userQueryParams: UserQueryParam
}

export enum TextQueryTypes {
  MML = "similar-mml",
  MLT = "similar-mlt"
}

export type UserQueryParam = {
  factor: number,
  type: TextQueryTypes,
  filterChannel: boolean
}

export type ElasticClientQueryParams = {
  from?: number,
  size?: number,
  factor?: number,
  channelId?: string
};

export type ElasticClientQueryResponse = {
  _id: string,
  _score: number,
  _source: {
    channelId: string,
    channelName: string,
    author: string,
    embed?: string,
    createdDate: string,
    en?: string,
    de?: string,
    hu?: string,
    lang: "en" | "de" | "hu",
  }
}

export type ElasticChannel = {
  channelId: string,
  channelName: string
}

export type ElasticChannelInfoParams = ElasticChannel | undefined;

export type ElasticChannelInfoResponse = {
  channels: ElasticChannel[],
  after_key: ElasticChannel
}