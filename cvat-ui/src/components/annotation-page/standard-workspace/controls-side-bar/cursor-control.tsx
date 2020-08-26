// Copyright (C) 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT

import React from 'react';
import Icon from 'antd/lib/icon';
import Tooltip from 'antd/lib/tooltip';

import { CursorIcon } from 'icons';
import { ActiveControl } from 'reducers/interfaces';
import { Canvas } from 'cvat-canvas-wrapper';

interface Props {
    canvasInstance: Canvas;
    cursorShortkey: string;
    activeControl: ActiveControl;
}

function CursorControl(props: Props): JSX.Element {
    const {
        canvasInstance,
        activeControl,
        cursorShortkey,
    } = props;

    return (
        <Tooltip title={`Cursor ${cursorShortkey}`} placement='right'>
            <Icon
                component={CursorIcon}
                className={activeControl === ActiveControl.CURSOR
                    ? 'cvat-active-canvas-control' : ''}
                onClick={
                    activeControl !== ActiveControl.CURSOR
                        ? (): void => canvasInstance.cancel()
                        : undefined
                }
            />
        </Tooltip>
    );
}

export default React.memo(CursorControl);
