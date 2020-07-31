// Copyright (C) 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT

import { PluginsActionTypes, PluginActions } from 'actions/plugins-actions';
import { registerGitPlugin } from 'utils/git-utils';
import { registerDEXTRPlugin } from 'utils/dextr-utils';
import {
    PluginsState,
} from './interfaces';

const defaultState: PluginsState = {
    fetching: false,
    initialized: false,
    list: {
        GIT_INTEGRATION: false,
        AUTO_ANNOTATION: false,
        TF_ANNOTATION: false,
        TF_SEGMENTATION: false,
        DEXTR_SEGMENTATION: false,
        ANALYTICS: false,
        REID: false,
    },
};

export default function (
    state: PluginsState = defaultState,
    action: PluginActions,
): PluginsState {
    switch (action.type) {
        case PluginsActionTypes.CHECK_PLUGINS: {
            return {
                ...state,
                initialized: false,
                fetching: true,
            };
        }
        case PluginsActionTypes.CHECKED_ALL_PLUGINS: {
            const { list } = action.payload;

            if (!state.list.GIT_INTEGRATION && list.GIT_INTEGRATION) {
                registerGitPlugin();
            }

            if (!state.list.DEXTR_SEGMENTATION && list.DEXTR_SEGMENTATION) {
                registerDEXTRPlugin();
            }

            return {
                ...state,
                initialized: true,
                fetching: false,
                list,
            };
        }
        default:
            return state;
    }
}
