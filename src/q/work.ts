/*
 * Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import Q from './';
const uuid = require('UUID');

export type DataCallback = (data: String) => any;

/**
 * <insert obligatory Rhianna jokes>
 */
export default class WorkQ {
  protected _personalQueue: string = uuid.v1();

  constructor(protected queue: Q) {
  }

  /**
   * TODO: need a way to acknowledge reads.
   */
  blockingRead(): Promise<string> {
    return this.queue.transfer(this._personalQueue);
  }
};
