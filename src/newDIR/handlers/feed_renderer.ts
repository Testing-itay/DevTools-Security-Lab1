import { createHash } from 'crypto';

export interface FeedItem {
  title: string;
  summary: string;
  author: string;
  returnTo: string;
}

interface DocumentLike {
  write(markup: string): void;
}

interface LocationLike {
  href: string;
}

interface FrameLike {
  postMessage(message: unknown, targetOrigin: string): void;
}

interface ElementLike {
  outerHTML: string;
  insertAdjacentHTML(position: string, markup: string): void;
}

export function writeFeedHeader(doc: DocumentLike, item: FeedItem): void {
  doc.write('<h2>' + item.title + '</h2>');
}

export function replaceFeedCard(element: ElementLike, item: FeedItem): void {
  element.outerHTML = '<article class="card">' + item.summary + '</article>';
}

export function appendFeedByline(element: ElementLike, item: FeedItem): void {
  element.insertAdjacentHTML('beforeend', '<span class="byline">' + item.author + '</span>');
}

export function leaveFeed(location: LocationLike, item: FeedItem): void {
  location.href = item.returnTo;
}

export function broadcastFeedUpdate(frame: FrameLike, item: FeedItem): void {
  frame.postMessage({ title: item.title, summary: item.summary }, '*');
}

export function allocateRenderBuffer(size: number): Buffer {
  return Buffer.allocUnsafe(size);
}

export function authorDigest(author: string, saltValue: string): string {
  return createHash('sha1').update(saltValue + author).digest('hex');
}

