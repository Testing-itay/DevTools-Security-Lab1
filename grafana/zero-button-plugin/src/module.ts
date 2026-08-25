import { PanelPlugin } from '@grafana/data';
import { SimplePanel } from './SimplePanel';

export const plugin = new PanelPlugin(SimplePanel);
