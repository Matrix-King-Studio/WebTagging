// Copyright (C) 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT

import React from 'react';
import Menu, { ClickParam } from 'antd/lib/menu';
import Modal from 'antd/lib/modal';

import DumpSubmenu from 'components/actions-menu/dump-submenu';
import LoadSubmenu from 'components/actions-menu/load-submenu';
import ExportSubmenu from 'components/actions-menu/export-submenu';
import ReIDPlugin from './reid-plugin';

interface Props {
    taskMode: string;
    loaders: string[];
    dumpers: string[];
    loadActivity: string | null;
    dumpActivities: string[] | null;
    exportActivities: string[] | null;
    installedReID: boolean;
    taskID: number;
    onClickMenu(params: ClickParam, file?: File): void;
}

export enum Actions {
    DUMP_TASK_ANNO = 'dump_task_anno',
    LOAD_JOB_ANNO = 'load_job_anno',
    EXPORT_TASK_DATASET = 'export_task_dataset',
    REMOVE_ANNO = 'remove_anno',
    OPEN_TASK = 'open_task',
}

export default function AnnotationMenuComponent(props: Props): JSX.Element {
    const {
        taskMode,
        loaders,
        dumpers,
        onClickMenu,
        loadActivity,
        dumpActivities,
        exportActivities,
        installedReID,
        taskID,
    } = props;

    let latestParams: ClickParam | null = null;
    function onClickMenuWrapper(params: ClickParam | null, file?: File): void {
        const copyParams = params || latestParams;
        if (!copyParams) {
            return;
        }
        latestParams = params;

        if (copyParams.keyPath.length === 2) {
            const [, action] = copyParams.keyPath;
            if (action === Actions.LOAD_JOB_ANNO) {
                if (file) {
                    Modal.confirm({
                        title: 'Current annotation will be lost',
                        content: 'You are going to upload new annotations to this job. Continue?',
                        onOk: () => {
                            onClickMenu(copyParams, file);
                        },
                        okButtonProps: {
                            type: 'danger',
                        },
                        okText: 'Update',
                    });
                }
            } else {
                onClickMenu(copyParams);
            }
        } else if (copyParams.key === Actions.REMOVE_ANNO) {
            Modal.confirm({
                title: 'All annotations will be removed',
                content: 'You are going to remove all annotations from the client. '
                    + 'It will stay on the server till you save a job. Continue?',
                onOk: () => {
                    onClickMenu(copyParams);
                },
                okButtonProps: {
                    type: 'danger',
                },
                okText: 'Delete',
            });
        } else {
            onClickMenu(copyParams);
        }
    }

    return (
        <Menu onClick={onClickMenuWrapper} className='cvat-annotation-menu' selectable={false}>
            {
                DumpSubmenu({
                    taskMode,
                    dumpers,
                    dumpActivities,
                    menuKey: Actions.DUMP_TASK_ANNO,
                })
            }
            {
                LoadSubmenu({
                    loaders,
                    loadActivity,
                    onFileUpload: (file: File): void => {
                        onClickMenuWrapper(null, file);
                    },
                    menuKey: Actions.LOAD_JOB_ANNO,
                })
            }
            {
                ExportSubmenu({
                    exporters: dumpers,
                    exportActivities,
                    menuKey: Actions.EXPORT_TASK_DATASET,
                })
            }

            <Menu.Item key={Actions.REMOVE_ANNO}>
                Remove annotations
            </Menu.Item>
            <Menu.Item key={Actions.OPEN_TASK}>
                <a href={`/tasks/${taskID}`} onClick={(e: React.MouseEvent) => e.preventDefault()}>
                    Open the task
                </a>
            </Menu.Item>
            { installedReID && <ReIDPlugin /> }
        </Menu>
    );
}
